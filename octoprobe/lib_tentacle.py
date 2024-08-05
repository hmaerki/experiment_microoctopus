from __future__ import annotations

import dataclasses
import io
import logging
import time
from collections.abc import Iterator
from contextlib import contextmanager

from usbhubctl import DualConnectedHub, Hub

from octoprobe import util_usb_serial
from octoprobe.infrastructure_tutorial.config_constants import EnumFut
from octoprobe.lib_infra_mcu import McuInfra

from . import util_power
from .lib_mpremote import MpRemote
from .util_baseclasses import TentacleSpec
from .util_constants import DIRECTORY_DOWNLOADS
from .util_dut_mcu import DutMcu, TAG_MCU, dut_mcu_factory
from .util_dut_programmers import DutProgrammer, FirmwareSpec, dut_programmer_factory
from .util_pyudev import UdevEventBase, UdevPoller
from .util_rp2 import (
    UDEV_FILTER_RP2_APPLICATION_MODE,
    UDEV_FILTER_RP2_BOOT_MODE,
    UdevApplicationModeEvent,
    rp2_flash_micropython,
)

logger = logging.getLogger(__file__)


class Tentacle[T]:
    RELAY_COUNT = 5
    LIST_ALL_RELAYS = list(range(1, RELAY_COUNT + 1))

    @staticmethod
    def is_valid_relay_index(i: int) -> bool:
        return 1 <= i <= Tentacle.RELAY_COUNT

    def __init__(
        self,
        tentacle_serial_number: str,
        tentacle_spec: TentacleSpec[T],
    ) -> None:
        self.tentacle_serial_number = tentacle_serial_number
        self.tentacle_spec = tentacle_spec
        self.hub: util_usb_serial.QueryResultTentacle | None = None
        self.mp_remote_infra: MpRemote | None = None
        self.mp_remote_dut: MpRemote | None = None
        self._dut_programmer: DutProgrammer | None = None
        self._dut_mcu: DutMcu | None = None
        self._power: util_power.TentaclePlugsPower | None = None
        self.mcu_infra: McuInfra = McuInfra(self)

    def __post_init__(self) -> None:
        assert (
            self.tentacle_serial_number == self.tentacle_serial_number.lower()
        ), f"Must not contain upper case letters: {self.tentacle_serial_number}"

    @property
    def description_short(self) -> str:
        f = io.StringIO()
        f.write(f"Label {self.tentacle_spec.label}\n")
        f.write(f"  tentacle_serial_number {self.tentacle_serial_number}\n")

        return f.getvalue()

    def _label(self, dut_or_infra: str) -> str:
        return f"Tentacle {dut_or_infra} {self.tentacle_serial_number}({self.tentacle_spec.label})"

    def has_required_futs(self, required_futs: list[EnumFut]) -> bool:
        for required_fut in required_futs:
            if required_fut in self.tentacle_spec.futs:
                return True
        return False

    @property
    def dut_programmer(self) -> DutProgrammer:
        if self._dut_programmer is None:
            self._dut_programmer = dut_programmer_factory(tags=self.tentacle_spec.tags)
        return self._dut_programmer

    @property
    def dut_mcu(self) -> DutMcu:
        if self._dut_mcu is None:
            self._dut_mcu = dut_mcu_factory(tags=self.tentacle_spec.tags)
        return self._dut_mcu

    @property
    def power(self) -> util_power.TentaclePlugsPower:
        assert self.hub is not None
        if self._power is None:
            self._power = util_power.TentaclePlugsPower(
                hub_location=self.hub.hub_location
            )
        return self._power

    @property
    def label(self) -> str:
        return self._label(dut_or_infra="")

    @property
    def label_dut(self) -> str:
        return self._label(dut_or_infra="DUT ")

    @property
    def label_infra(self) -> str:
        return self._label(dut_or_infra="INFRA ")

    def power_dut_off_and_wait(self) -> None:
        """
        Use this instead of 'self.power.dut = False'
        """
        if self.power.dut:
            self.power.dut = False
            self.mp_remote_dut = None
            time.sleep(0.5)

    def assign_connected_hub(
        self,
        query_result_tentacle: util_usb_serial.QueryResultTentacle,
    ) -> None:
        assert isinstance(query_result_tentacle, util_usb_serial.QueryResultTentacle)
        self.hub = query_result_tentacle

    @property
    def pytest_id(self) -> str:
        name = self.tentacle_spec.tentacle_type.name
        if name.startswith("TENTACLE_MCU"):
            name = self.tentacle_spec.get_property(TAG_MCU)
            assert name is not None
        name = name.replace("TENTACLE_DEVICE_", "").replace("TENTACLE_", "")
        return name + "_" + self.tentacle_serial_number[-4:]

    def get_property(self, tag: str) -> str | None:
        return self.tentacle_spec.get_property(tag=tag)

    @property
    @contextmanager
    def active_led(self) -> None:
        try:
            self.mcu_infra.active_led(on=True)
            yield
        finally:
            self.mcu_infra.active_led(on=False)

    def boot_and_init_mp_remote_dut(self, udev: UdevPoller) -> None:
        assert self.mp_remote_dut is None
        tty = self.dut_mcu.application_mode_power_up(tentacle=self, udev=udev)
        self.mp_remote_dut = MpRemote(tty=tty)

    def dut_installed_firmware_version(self) -> str:
        """
        Example:
        >>> import sys
        >>> sys.version
        '3.4.0; MicroPython v1.20.0 on 2023-04-26'
        """
        assert self.mp_remote_dut is not None
        version = self.mp_remote_dut.exec_raw("import sys; print(sys.version)")
        return version.strip()

    def dut_required_firmware_already_installed(
        self,
        firmware_spec: FirmwareSpec,
        exception_text: str | None = None,
    ) -> bool:
        installed_version = self.dut_installed_firmware_version()
        assert isinstance(firmware_spec, FirmwareSpec)
        versions_equal = firmware_spec.micropython_version_text == installed_version
        if exception_text is not None:
            if not versions_equal:
                raise ValueError(
                    f"{exception_text}: Version installed '{installed_version}', but expected '{firmware_spec.micropython_version_text}'!"
                )
        return versions_equal

    def flash_dut(self, udev: UdevPoller, firmware_spec: FirmwareSpec) -> None:
        assert self.hub is not None
        assert isinstance(firmware_spec, FirmwareSpec)

        try:
            self.boot_and_init_mp_remote_dut(udev=udev)
            if self.dut_required_firmware_already_installed(
                firmware_spec=firmware_spec
            ):
                logger.info(f"{self.label_dut}: firmware is already installed")
                return

        except TimeoutError as e:
            logger.debug(f"DUT seems not to have firmware installed: {e!r}")

        tty = self.dut_programmer.flash(
            tentacle=self,
            udev=udev,
            firmware_spec=firmware_spec,
        )
        self.mp_remote_dut = MpRemote(tty=tty)

        self.dut_required_firmware_already_installed(
            firmware_spec=firmware_spec,
            exception_text=f"DUT: After installing {firmware_spec.filename}",
        )

    def dut_power_off(self) -> None:
        self.power.dut = False
        self.mp_remote_dut = None

    def rp2_test_mp_remote(self) -> None:
        assert self.mp_remote_infra is None
        assert self.hub is not None
        assert self.hub.rp2_serial_port is not None
        self.mp_remote_infra = MpRemote(tty=self.hub.rp2_serial_port)
        mp_program = """
import machine
import ubinascii

def get_unique_id():
    return ubinascii.hexlify(machine.unique_id()).decode('ascii')
"""
        self.mp_remote_infra.exec_raw(mp_program)
        unique_id = self.mp_remote_infra.exec_raw("print(get_unique_id())")
        unique_id = unique_id.strip()
        assert self.hub.rp2_serial_number == unique_id

        main_exists = self.mp_remote_infra.exec_raw(
            "import os; print('main.py' in os.listdir())"
        )
        if eval(main_exists):
            raise ValueError(f"{self.label_infra}: Found 'main.py': Please remove it!")

    def rp2_get_unique_id_obsolete(self, event: UdevEventBase) -> str:
        assert isinstance(event, UdevApplicationModeEvent)

        assert self.mp_remote_infra is None
        self.mp_remote_infra = MpRemote(tty=event.tty)
        print(f"Event: {event!r}")
        mp_program = """
import machine
import ubinascii

def get_unique_id():
    return ubinascii.hexlify(machine.unique_id()).decode('ascii').upper()
"""
        self.mp_remote_infra.exec_raw(mp_program)
        unique_id = self.mp_remote_infra.exec_raw("print(get_unique_id())")
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
        assert unique_id == self.tentacle_serial_number


@dataclasses.dataclass
class Tentacles:
    tentacles: list[Tentacle]

    @property
    def plugs_infra(self) -> Iterator[UsbPlug]:
        for tentacle in self.tentacles:
            if tentacle.plug_infra is None:
                continue
            yield tentacle.plug_infra

    @property
    def plugs_dut(self) -> Iterator[UsbPlug]:
        for tentacle in self.tentacles:
            if tentacle.plug_dut is None:
                continue
            yield tentacle.plug_dut


@dataclasses.dataclass
class UsbHub:
    label: str
    model: Hub
    connected_hub: None | DualConnectedHub = None

    def get_plug(self, plug_number: int) -> UsbPlug:
        assert (
            1 <= plug_number <= self.model.plug_count
        ), f"{self.model.model}: Plug {plug_number} does not exit! Valid plugs [0..{self.model.plug_count}]."
        return UsbPlug(usb_hub=self, plug_number=plug_number)

    def setup(self) -> None:
        connected_hubs = self.model.find_connected_dualhubs()
        self.connected_hub = connected_hubs.expect_one()

    def teardown(self) -> None:
        pass

    @property
    def description_short(self) -> str:
        f = io.StringIO()
        f.write(f"Label {self.label}\n")
        f.write(f"  Model {self.model.model}\n")
        return f.getvalue()


@dataclasses.dataclass
class UsbPlug:
    usb_hub: UsbHub
    plug_number: int

    @property
    def description_short(self) -> str:
        return f"plug {self.plug_number} on '{self.usb_hub.label}' ({self.usb_hub.model.model})"

    @property
    def power(self) -> bool:
        raise NotImplementedError()

    @power.setter
    def power(self, on: bool) -> None:
        c = self.usb_hub.connected_hub
        assert c is not None
        c.get_plug(plug_number=self.plug_number).power(on=on)
