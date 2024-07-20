from __future__ import annotations
import typing

if typing.TYPE_CHECKING:
    from octoprobe.lib_tentacle import Tentacle


class McuInfra:
    BASE_CODE = """
from machine import Pin

pin_led_active = Pin('GPIO24', Pin.OUT)

pin_relays = {
    1: Pin('GPIO1', Pin.OUT),
    2: Pin('GPIO2', Pin.OUT),
    3: Pin('GPIO3', Pin.OUT),
    4: Pin('GPIO4', Pin.OUT),
    5: Pin('GPIO8', Pin.OUT),
}

def set_relays(list_relays):
    for i, close  in list_relays:
        pin_relays[i].value(close)
"""

    def __init__(self, tentacle: Tentacle) -> None:
        self._tentacle = tentacle
        self._base_code_loaded = False

    def _load_base_code(self) -> None:
        if self._base_code_loaded:
            return
        assert self._tentacle.mp_remote_infra is not None
        self._tentacle.mp_remote_infra.exec_raw(self.BASE_CODE)

    def relays(
        self,
        relays_close: list[int] | None = None,
        relays_open: list[int] | None = None,
    ) -> None:
        if relays_close is None:
            relays_close = []
        if relays_open is None:
            relays_open = []
        assert isinstance(relays_close, list)
        assert isinstance(relays_open, list)
        self._load_base_code()
        for i in relays_close + relays_open:
            assert self._tentacle.is_valid_relay_index(i)
        list_relays = [(number, True) for number in relays_close] + [
            (number, False) for number in relays_open
        ]

        self._tentacle.mp_remote_infra.exec_raw(cmd=f"set_relays({list_relays})")

    def active_led(self, on: bool) -> None:
        assert isinstance(on, bool)
        self._load_base_code()

        self._tentacle.mp_remote_infra.exec_raw(cmd=f"pin_led_active.value({int(on)})")
