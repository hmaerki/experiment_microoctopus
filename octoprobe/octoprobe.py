from __future__ import annotations

import time

from octoprobe import util_usb_serial
from octoprobe.util_power import UsbPlug, UsbPlugs

from .lib_infrastructure import Infrastructure
from .lib_tentacle import Tentacle, Tentacles
from .util_pyudev import UdevPoller


class NTestRun:
    """
    'TestRun' would be collected by pytest: So we name it 'NTestRun'
    """

    def __init__(
        self,
        infrastructure: Infrastructure,
    ) -> None:
        assert isinstance(infrastructure, Infrastructure)
        self.infrastructure = infrastructure
        self._udev_poller: UdevPoller | None = None

    @property
    def udev_poller(self) -> UdevPoller:
        if self._udev_poller is None:
            self._udev_poller = UdevPoller()
        return self._udev_poller

    def session_powercycle_tentacles(self) -> None:
        """
        Powers all RP2 infra.
        Finds all tentacle by finding rp2_unique_id of the RP2 infra.
        """
        # We have to reset the power for all rp2-infra to become visible
        hubs = util_usb_serial.QueryResultTentacle.query(verbose=False)
        hubs = hubs.select(serials=None)
        hubs.power(plugs=UsbPlugs.default_off())
        time.sleep(0.2)  # success: 0.0
        hubs.power(plugs=UsbPlugs({UsbPlug.INFRA: True}))
        # Without hub inbetween: failed: 0.4, success: 0.5
        # With hub inbetween: failed: 0.7, success: 0.8
        time.sleep(1.2)

        hubs = util_usb_serial.QueryResultTentacle.query(verbose=True)
        for tentacle in self.infrastructure.tentacles:
            query_result_tentacle = hubs.get(
                serial_number=tentacle.tentacle_serial_number
            )
            tentacle.assign_connected_hub(query_result_tentacle=query_result_tentacle)

    def function_setup_infra(self) -> None:
        """
        Power off all other known usb power plugs
        For each active tentacle:
          Power on infa
          Flash firmware
          Get serial numbers and assert if it does not match the config
          Return tty
        """

        # Instantiate poller BEFORE switching on power to avoid a race condition
        for tentacle in self.infrastructure.tentacles:
            tentacle.setup_infra(self.udev_poller)

    def function_teardown(self) -> None:
        for tentacle in self.infrastructure.tentacles:
            tentacle.dut_power_off()

    def session_teardown(self) -> None:
        if self._udev_poller is not None:
            self._udev_poller.close()
            self._udev_poller = None

    def function_prepare_dut(self) -> None:
        for tentacle in self.infrastructure.tentacles:
            tentacle.power.dut = False
            if tentacle.mp_remote_infra is not None:
                tentacle.mp_remote_infra.close()
                tentacle.mp_remote_infra = None
            if tentacle.mp_remote_dut is not None:
                tentacle.mp_remote_dut.close()
                tentacle.mp_remote_dut = None

    def function_setup_dut(self, active_tentacles: list[Tentacles]) -> None:
        for tentacle in active_tentacles:
            with tentacle.active_led:
                tentacle.flash_dut(udev=self.udev_poller)

    def function_teardown_dut(self, active_tentacles: list[Tentacles]) -> None:
        for tentacle in active_tentacles:
            tentacle.power_dut_off_and_wait()

    def function_teardown_infra(self, active_tentacles: list[Tentacles]) -> None:
        for tentacle in active_tentacles:
            tentacle.mcu_infra.relays(relays_open=tentacle.LIST_ALL_RELAYS)

    def setup_relays(self, tentacles: list[Tentacle], futs: tuple[EnumFut]) -> None:
        assert isinstance(tentacles, list | tuple)
        assert isinstance(futs, list | tuple)
        assert len(futs) == 1
        fut = futs[0]
        for tentacle in tentacles:
            list_relays = tentacle.tentacle_spec.relays_closed[fut]
            tentacle.mcu_infra.relays(relays_close=list_relays)
