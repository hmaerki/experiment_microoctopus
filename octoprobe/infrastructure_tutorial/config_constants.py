"""
Constants required by this infrastructure.
"""

import enum


class TentacleType(enum.StrEnum):
    TENTACLE_MCU = enum.auto()
    TENTACLE_DEVICE_POTPOURRY = enum.auto()
    TENTACLE_DAQ_SALEAE = enum.auto()


class EnumFut(enum.StrEnum):
    FUT_I2C = enum.auto()
    FUT_UART = enum.auto()
    FUT_ONEWIRE = enum.auto()
    FUT_TIMER = enum.auto()
