from __future__ import annotations

import logging
import time

from . import util_power, util_usb_serial
from .lib_mpremote import MpRemote
from .lib_tentacle_infra_rp2 import InfraRP2
from .util_constants import DIRECTORY_DOWNLOADS
from .util_pyudev import UdevEventBase, UdevPoller
from .util_rp2 import (
    UDEV_FILTER_RP2_APPLICATION_MODE,
    UDEV_FILTER_RP2_BOOT_MODE,
    UdevApplicationModeEvent,
    rp2_flash_micropython,
)

logger = logging.getLogger(__file__)


class TentacleInfra:
    """
    The Infrastructure side of a tentacle PCB.

    * Allows to program the RP2
    * Allows to run micropython code on the RP2.
    """

    RELAY_COUNT = 5
    LIST_ALL_RELAYS = list(range(1, RELAY_COUNT + 1))

    @staticmethod
    def is_valid_relay_index(i: int) -> bool:
        return 1 <= i <= TentacleInfra.RELAY_COUNT

    def __init__(self, label: str) -> None:
        assert isinstance(label, str)
        self.label = label
        self.hub: util_usb_serial.QueryResultTentacle | None = None
        self._mp_remote: MpRemote | None = None
        self._power: util_power.TentaclePlugsPower | None = None
        self.mcu_infra: InfraRP2 = InfraRP2(self)

    def assign_connected_hub(
        self,
        query_result_tentacle: util_usb_serial.QueryResultTentacle,
    ) -> None:
        assert isinstance(query_result_tentacle, util_usb_serial.QueryResultTentacle)
        self.hub = query_result_tentacle

    def mp_remote_close(self) -> None:
        if self._mp_remote is None:
            return
        self._mp_remote.close()
        self._mp_remote = None

    @property
    def mp_remote(self) -> MpRemote:
        assert self._mp_remote is not None
        return self._mp_remote

    @property
    def power(self) -> util_power.TentaclePlugsPower:
        assert self.hub is not None
        if self._power is None:
            self._power = util_power.TentaclePlugsPower(
                hub_location=self.hub.hub_location
            )
        return self._power

    def power_dut_off_and_wait(self) -> None:
        """
        Use this instead of 'self.power.dut = False'
        """
        if self.power.dut:
            self.power.dut = False
            time.sleep(0.5)

    def rp2_test_mp_remote(self) -> None:
        assert self._mp_remote is None
        assert self.hub is not None
        assert self.hub.rp2_serial_port is not None
        self._mp_remote = MpRemote(tty=self.hub.rp2_serial_port)
        mp_program = """
import machine
import ubinascii

def get_unique_id():
    return ubinascii.hexlify(machine.unique_id()).decode('ascii')
"""
        self._mp_remote.exec_raw(mp_program)
        unique_id = self._mp_remote.exec_raw("print(get_unique_id())")
        unique_id = unique_id.strip()
        assert self.hub.rp2_serial_number == unique_id

        main_exists = self._mp_remote.exec_raw(
            "import os; print('main.py' in os.listdir())"
        )
        if eval(main_exists):
            raise ValueError(f"{self.label}: Found 'main.py': Please remove it!")

    def rp2_get_unique_id_obsolete(self, event: UdevEventBase) -> str:
        assert isinstance(event, UdevApplicationModeEvent)

        assert self._mp_remote is None
        self._mp_remote = MpRemote(tty=event.tty)
        print(f"Event: {event!r}")
        mp_program = """
import machine
import ubinascii

def get_unique_id():
    return ubinascii.hexlify(machine.unique_id()).decode('ascii').upper()
"""
        self._mp_remote.exec_raw(mp_program)
        unique_id = self._mp_remote.exec_raw("print(get_unique_id())")
        return unique_id.strip()

    def setup_infra(self, udev: UdevPoller) -> None:
        self.rp2_test_mp_remote()
        return

        if self.hub is None:
            return

        with udev.guard as guard:
            self.power_(plugs={util_power.UsbPlug.INFRA, True})

            event = guard.expect_event(
                UDEV_FILTER_RP2_BOOT_MODE,
                text_where=self.label_infra,
                text_expect="Expect RP2 in programming mode to become visible on udev after power on",
                timeout_s=2.0,
            )

        with udev.guard as guard:
            rp2_flash_micropython(event, DIRECTORY_DOWNLOADS / "firmware.uf2")

            event = udev.expect_event(
                UDEV_FILTER_RP2_APPLICATION_MODE,
                text_where=self.label_infra,
                text_expect="Expect RP2 in application mode to become visible on udev after programming ",
                timeout_s=3.0,
            )

        unique_id = self.rp2_get_unique_id(event)
        assert unique_id == self.serial
