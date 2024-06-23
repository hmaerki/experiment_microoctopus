import abc
import pathlib
import time
import typing

from usbhubctl.util_subprocess import subprocess_run

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
    from .lib_tentacle import Tentacle, UsbPlug
    from .util_pyudev import UdevPoller

TAG_PROGRAMMER = "programmer"


class DutProgrammer(abc.ABC):
    @abc.abstractmethod
    def flash(
        self, tentacle: "Tentacle", udev: "UdevPoller", plug: "UsbPlug"
    ) -> str: ...


class DutProgrammerDfuUtil(DutProgrammer):
    def flash(self, tentacle: "Tentacle", udev: "UdevPoller", plug: "UsbPlug") -> str:
        """
        Example return: /dev/ttyACM1
        """
        tentacle.infra_relay(number=1, close=True)

        with udev.guard as guard:
            plug.power = True

            event = guard.expect_event(
                UDEV_FILTER_PYBOARD_BOOT_MODE,
                text_where=tentacle.label_dut,
                text_expect="Expect mcu to become visible on udev after power on",
                timeout_s=3.0,
            )

        print(f"EVENT PYBOARD: {event}")
        assert isinstance(event, UdevBootModeEvent)
        filename_dfu = pathlib.Path.home() / "Downloads" / "PYBV11-20230426-v1.20.0.dfu"
        assert filename_dfu.is_file()
        args = [
            "dfu-util",
            "--serial",
            event.serial,
            "--download",
            str(filename_dfu),
        ]
        subprocess_run(args=args, timeout_s=60.0)

        tentacle.infra_relay(number=1, close=False)

        with udev.guard as guard:
            plug.power = False
            plug.power = True

            event = guard.expect_event(
                UDEV_FILTER_PYBOARD_APPLICATION_MODE,
                text_where=tentacle.label_dut,
                text_expect="Expect mcu to become visible on udev after DfuUtil programming",
                timeout_s=3.0,
            )

        print(f"EVENT PYBOARD: {event}")
        assert isinstance(event, UdevApplicationModeEvent)
        tty = event.tty
        assert isinstance(tty, str)
        return tty


class DutProgrammerPicotool(DutProgrammer):
    def flash(self, tentacle: "Tentacle", udev: "UdevPoller", plug: "UsbPlug") -> str:
        """
        Example return: /dev/ttyACM1
        """
        # Press Boot Button
        tentacle.infra_relay(number=1, close=True)

        with udev.guard as guard:
            plug.power = True

            event = guard.expect_event(
                UDEV_FILTER_RP2_BOOT_MODE,
                text_where=tentacle.label_dut,
                text_expect="Expect RP2 to become visible on udev after power on",
                timeout_s=2.0,
            )

        # Release Boot Button
        tentacle.infra_relay(number=1, close=False)

        print(f"EVENT RP2: {event}")
        with udev.guard as guard:
            rp2_flash_micropython(
                event, DIRECTORY_DOWNLOADS / "RPI_PICO-20240222-v1.22.2.uf2"
            )

            event = udev.expect_event(
                UDEV_FILTER_RP2_APPLICATION_MODE,
                text_where=tentacle.label_dut,
                text_expect="Expect RP2 to become visible on udev after power on",
                timeout_s=4.0,
            )

        with udev.guard as guard:
            plug.power = False
            plug.power = True

            event = guard.expect_event(
                UDEV_FILTER_RP2_APPLICATION_MODE,
                text_where=tentacle.label_dut,
                text_expect="Expect RP2 to become visible on udev after power on",
                timeout_s=3.0,
            )

        print(f"EVENT RP2: {event}")
        assert isinstance(event, UdevApplicationModeEvent)
        tty = event.tty
        assert isinstance(tty, str)

        # TODO: Why?
        time.sleep(2.0)
        return tty


def programmer_factory(tags: str) -> None | DutProgrammer:
    """
    Example 'tags': programmer=picotool,xy=5
    """
    programmer = PropertyString(tags).get_tag(TAG_PROGRAMMER)
    if programmer is None:
        return None
    if programmer == "picotool":
        return DutProgrammerPicotool()
    if programmer == "dfu-util":
        return DutProgrammerDfuUtil()
    raise ValueError(f"Unknown '{programmer}' in '{tags}'!")
