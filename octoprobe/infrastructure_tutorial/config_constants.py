"""
Constants required by this infrastructure.
"""

from __future__ import annotations

import enum
import typing

if typing.TYPE_CHECKING:
    from octoprobe.lib_tentacle import Tentacle


class TentacleType(enum.StrEnum):
    TENTACLE_MCU = enum.auto()
    TENTACLE_DEVICE_POTPOURRY = enum.auto()
    TENTACLE_DAQ_SALEAE = enum.auto()

    def get_tentacles_for_type(
        self,
        tentacles: list[Tentacle],
        required_futs: list[EnumFut],
    ) -> list[Tentacle]:
        """
        Select all tentacles which correspond to this
        TentacleType and list[EnumFut].
        """

        def has_required_futs(t: Tentacle) -> bool:
            for required_fut in required_futs:
                if required_fut in t.tentacle_spec.futs:
                    return True
            return False

        return [
            t
            for t in tentacles
            if (t.tentacle_spec.tentacle_type is self) and (has_required_futs(t))
        ]


class EnumFut(enum.StrEnum):
    FUT_I2C = enum.auto()
    FUT_UART = enum.auto()
    FUT_ONEWIRE = enum.auto()
    FUT_TIMER = enum.auto()
