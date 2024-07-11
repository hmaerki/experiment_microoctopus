from __future__ import annotations

import dataclasses
import enum

from usbhubctl import Location, util_octohub4


class PowerCycle(str, enum.Enum):
    INFRA = "infra"
    INFRBOOT = "infraboot"
    DUT = "dut"
    OFF = "off"


class UsbPlug(str, enum.Enum):
    INFRA = "infra"
    INFRABOOT = "infraboot"
    DUT = "dut"
    ERROR = "error"

    @property
    def nummer(self) -> int:
        """
        Return the plug/port number from 1 to 4
        """
        return {
            UsbPlug.INFRA: 1,
            UsbPlug.INFRABOOT: 2,
            UsbPlug.DUT: 3,
            UsbPlug.ERROR: 4,
        }[self]


@dataclasses.dataclass
class UsbPlugs:
    plugs: dict[UsbPlug, bool] = dataclasses.field(default_factory=dict)

    _DICT_DEFAULT_OFF = {
        UsbPlug.INFRA: False,
        UsbPlug.INFRABOOT: True,
        UsbPlug.DUT: False,
        UsbPlug.ERROR: False,
    }

    def set_default_off(self) -> None:
        self.plugs = self._DICT_DEFAULT_OFF

    @property
    def text(self) -> str:
        plugs: list[str] = []
        for up in UsbPlug:
            try:
                plugs.append(self._get_text(up))
            except KeyError:
                continue
        return ",".join(plugs)

    def _get_text(self, up: UsbPlug) -> str:
        """
        Raise KeyError if UsbPower not found
        """
        v = self.plugs[up]
        sign = "+" if v else "-"
        return sign + up.value

    def power(self, hub_location: Location) -> None:
        connected_hub = util_octohub4.location_2_connected_hub(location=hub_location)
        for plug, on in self.plugs.items():
            p = connected_hub.get_plug(plug.nummer)
            p.power(on=on)

    @staticmethod
    def all_on() -> UsbPlugs:
        return UsbPlugs(plugs={p: True for p in UsbPlug})

    @staticmethod
    def all_off() -> UsbPlugs:
        return UsbPlugs(plugs={p: False for p in UsbPlug})

    @classmethod
    def default_off(cls) -> UsbPlugs:
        return UsbPlugs(plugs=cls._DICT_DEFAULT_OFF)
