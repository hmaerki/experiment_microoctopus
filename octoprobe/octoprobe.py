from __future__ import annotations

from .lib_infrastructure import Infrastructure
from .lib_tentacle import Tentacle, Tentacles
from .util_pyudev import UdevPoller


class Runner:
    def __init__(
        self,
        infrastructure: Infrastructure,
        active_tentacles: list[Tentacle],
        udev_poller: UdevPoller | None = None,
    ) -> None:
        assert isinstance(infrastructure, Infrastructure)
        self.infrastructure = infrastructure
        assert isinstance(active_tentacles, list | tuple)
        for tentacle in active_tentacles:
            assert (
                tentacle in infrastructure.tentacles
            ), f"Tentacle '{tentacle.label}' is missing in the infrastructure."
        self.active_tentacles = Tentacles(tentacles=active_tentacles)
        self.udev_poller = udev_poller

    def reset_infa_dut(self) -> None:
        for hub in self.infrastructure.hubs:
            hub.setup()

        for tentacle in self.infrastructure.tentacles:
            tentacle.reset_infa_dut()

    def setup_infra(self) -> None:
        """
        Power off all other known usb power plugs
        For each active tentacle:
          Power on infa
          Flash firmware
          Get serial numbers and assert if it does not match the config
          Return tty
        """
        assert self.udev_poller is None
        self.udev_poller = UdevPoller()

        # Instantiate poller BEFORE switching on power to avoid a race condition
        for tentacle in self.active_tentacles.tentacles:
            tentacle.setup_infra(self.udev_poller)

    def teardown(self) -> None:
        for tentacle in self.infrastructure.tentacles:
            tentacle.all_plugs_power_off()

        if self.udev_poller is not None:
            self.udev_poller.close()

    def setup_dut(self) -> None:
        assert self.udev_poller is not None
        for tentacle in self.active_tentacles.tentacles:
            tentacle.flash_dut(udev=self.udev_poller)
