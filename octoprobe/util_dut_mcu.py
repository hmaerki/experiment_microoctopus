import abc
import time
import typing

from octoprobe.util_baseclasses import PropertyString
from octoprobe.util_pyboard import UDEV_FILTER_PYBOARD_APPLICATION_MODE
from octoprobe.util_rp2 import (
    UdevApplicationModeEvent,
    UDEV_FILTER_RP2_APPLICATION_MODE,
)

TAG_MCU = "mcu"

if typing.TYPE_CHECKING:
    from .lib_tentacle import Tentacle
    from .util_pyudev import UdevPoller


class DutMcu(abc.ABC):
    @abc.abstractmethod
    def application_mode_power_up(
        self,
        tentacle: "Tentacle",
        udev: "UdevPoller",
    ) -> str:
        """
        Power up and wait for udev-event.
        Return tty of pybard
        """
        ...


class DutMicropythonSTM32(DutMcu):
    def application_mode_power_up(
        self, tentacle: "Tentacle", udev: "UdevPoller"
    ) -> str:
        """
        Power up and wait for udev-event.
        Return tty of pybard
        """
        tentacle.power_dut_off_and_wait()

        with udev.guard as guard:
            tentacle.power.dut = True

            event = guard.expect_event(
                UDEV_FILTER_PYBOARD_APPLICATION_MODE,
                text_where=tentacle.label_dut,
                text_expect="Expect mcu to become visible on udev after DfuUtil programming",
                timeout_s=3.0,
            )

        assert isinstance(event, UdevApplicationModeEvent)
        tty = event.tty
        assert isinstance(tty, str)
        return tty


class DutMicropythonRP2(DutMcu):
    def application_mode_power_up(
        self,
        tentacle: "Tentacle",
        udev: "UdevPoller",
    ) -> str:
        """
        Power up and wait for udev-event.
        Return tty of pybard
        """
        tentacle.power_dut_off_and_wait()

        with udev.guard as guard:
            tentacle.power.dut = True

            event = guard.expect_event(
                UDEV_FILTER_RP2_APPLICATION_MODE,
                text_where=tentacle.label_dut,
                text_expect="Expect RP2 to become visible",
                timeout_s=3.0,
            )

        assert isinstance(event, UdevApplicationModeEvent)
        tty = event.tty
        assert isinstance(tty, str)
        return tty


def dut_mcu_factory(tags: str) -> DutMcu:
    """
    Example 'tags': mcu=stm32,programmer=picotool,xy=5
    """
    mcu = PropertyString(tags).get_tag(TAG_MCU)
    if mcu is None:
        raise ValueError(f"No '{TAG_MCU}' specified in '{tags}'!")
    if mcu == "stm32":
        return DutMicropythonSTM32()
    if mcu == "rp2":
        return DutMicropythonRP2()
    raise ValueError(f"Unknown '{mcu}' in '{tags}'!")