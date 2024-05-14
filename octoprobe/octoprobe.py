"""
Preparation:
  sudo chown root:root octoprobe/downloads/picotool
  sudo chmod u+s octoprobe/downloads/picotool
"""

import dataclasses

from octoprobe.lib_mpremote import MpRemote
from .lib_infrastructure import Infrastructure
from .lib_tentacle import Tentacles
from .util_pyudev import UdevPoller
from .util_programmers import programmer_factory


@dataclasses.dataclass
class Runner:
    infrastructure: Infrastructure
    active_tentacles: Tentacles
    udev_poller: None | UdevPoller = None

    def __post_init__(self):
        assert isinstance(self.infrastructure, Infrastructure)
        if isinstance(self.active_tentacles, list | tuple):
            self.active_tentacles = Tentacles(tentacles=self.active_tentacles)
        assert isinstance(self.active_tentacles, Tentacles)

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
        for tentacle in self.active_tentacles.tentacles:
            tentacle.flash_dut(udev=self.udev_poller)
