import abc
import dataclasses
import pathlib
import time
import typing

from usbhubctl.util_subprocess import subprocess_run

from . import util_power, util_usb_serial
from .util_baseclasses import PropertyString
from .util_constants import DIRECTORY_DOWNLOADS
from .util_pyboard import (
    UDEV_FILTER_PYBOARD_APPLICATION_MODE,
    UDEV_FILTER_PYBOARD_BOOT_MODE,
)
from .util_rp2 import (
    UDEV_FILTER_RP2_APPLICATION_MODE,
    UDEV_FILTER_RP2_BOOT_MODE,
    UdevApplicationModeEvent,
    UdevBootModeEvent,
    rp2_flash_micropython,
)

if typing.TYPE_CHECKING:
    from .lib_tentacle import Tentacle
    from .util_pyudev import UdevPoller

TAG_PROGRAMMER = "programmer"


@dataclasses.dataclass
class FirmwareSpec:
    filename: pathlib.Path
    """
    Example: Downloads/PYBV11-20230426-v1.20.0.dfu
    """
    micropython_version_text: str | None
    """
    Example:
    >>> import sys
    >>> sys.version
    '3.4.0; MicroPython v1.20.0 on 2023-04-26'
    """


class DutProgrammer(abc.ABC):
    @abc.abstractmethod
    def flash(self, tentacle: "Tentacle", udev: "UdevPoller") -> str: ...


class DutProgrammerDfuUtil(DutProgrammer):
    def flash(self, tentacle: "Tentacle", udev: "UdevPoller") -> str:
        """
        Example return: /dev/ttyACM1
        """
        tentacle.mcu_infra.relays(relays_close=[1])

        tentacle.power_dut_off_and_wait()

        with udev.guard as guard:
            tentacle.power.dut = True

            event = guard.expect_event(
                UDEV_FILTER_PYBOARD_BOOT_MODE,
                text_where=tentacle.label_dut,
                text_expect="Expect mcu to become visible on udev after power on",
                timeout_s=3.0,
            )

        print(f"EVENT PYBOARD: {event}")
        assert isinstance(event, UdevBootModeEvent)
        assert tentacle.firmware_spec is not None
        filename_dfu = tentacle.firmware_spec.filename
        assert filename_dfu.is_file()
        args = [
            "dfu-util",
            "--serial",
            event.serial,
            "--download",
            str(filename_dfu),
        ]
        subprocess_run(args=args, timeout_s=60.0)

        tentacle.mcu_infra.relays(relays_open=[1])

        return tentacle.dut_mcu.application_mode_power_up(tentacle=tentacle, udev=udev)


class DutProgrammerPicotool(DutProgrammer):
    def flash(self, tentacle: "Tentacle", udev: "UdevPoller") -> str:
        """
        Example return: /dev/ttyACM1
        """
        tentacle.power_dut_off_and_wait()

        # Press Boot Button
        tentacle.mcu_infra.relays(relays_close=[1])

        with udev.guard as guard:
            tentacle.power.dut = True

            event = guard.expect_event(
                UDEV_FILTER_RP2_BOOT_MODE,
                text_where=tentacle.label_dut,
                text_expect="Expect RP2 to become visible on udev after power on",
                timeout_s=2.0,
            )

        # Release Boot Button
        tentacle.mcu_infra.relays(relays_open=[1])

        return tentacle.dut_mcu.application_mode_power_up(tentacle=tentacle, udev=udev)


def dut_programmer_factory(tags: str) -> DutProgrammer:
    """
    Example 'tags': programmer=picotool,xy=5
    """
    programmer = PropertyString(tags).get_tag(TAG_PROGRAMMER)
    if programmer is None:
        raise ValueError(f"No '{TAG_PROGRAMMER}' specified in '{tags}'!")
    if programmer == "picotool":
        return DutProgrammerPicotool()
    if programmer == "dfu-util":
        return DutProgrammerDfuUtil()
    raise ValueError(f"Unknown '{programmer}' in '{tags}'!")
