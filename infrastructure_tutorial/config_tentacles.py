from __future__ import annotations

import dataclasses

from octoprobe.util_baseclasses import TentacleSpec

from .config_constants import EnumFut, TentacleType


@dataclasses.dataclass
class McuConfig:
    """
    These variables will be replaced in micropython code
    """

    trig1: str
    trig2: str
    i2c: str
    onewire: str


DOC_TENTACLE_PYBOARD = """
See: https://github.com/hmaerki/experiment_microoctopus/tree/main/infrastructure_tutorial/tentacle_MCU_grobotics_pyboard
"""
tentacle_spec_pyboard = TentacleSpec(
    tentacle_type=TentacleType.TENTACLE_MCU,
    futs=[EnumFut.FUT_I2C, EnumFut.FUT_UART, EnumFut.FUT_ONEWIRE, EnumFut.FUT_TIMER],
    category="Micropython Board",
    label="pyboard_v1.0",
    doc=DOC_TENTACLE_PYBOARD,
    tags="board=PYBV11,mcu=stm32,programmer=dfu-util",
    relays_closed={
        EnumFut.FUT_I2C: [2, 3, 4, 5],
        EnumFut.FUT_ONEWIRE: [2, 3, 4],
    },
    mcu_config=McuConfig(
        trig1="Y2",
        trig2="Y3",
        i2c="i2c = I2C(scl='Y9', sda='Y10', freq=100000)",
        onewire="Y9",
    ),
)


DOC_TENTACLE_RASPBERRY_PICO = """
See: https://github.com/hmaerki/experiment_microoctopus/tree/main/infrastructure_tutorial/tentacle_MCU_raspberry_pico
"""
tentacle_spec_raspberry_pico = TentacleSpec(
    tentacle_type=TentacleType.TENTACLE_MCU,
    futs=[EnumFut.FUT_I2C, EnumFut.FUT_UART, EnumFut.FUT_ONEWIRE, EnumFut.FUT_TIMER],
    category="Micropython Board",
    label="raspberry_pico_v1.0",
    doc=DOC_TENTACLE_RASPBERRY_PICO,
    tags="board=RPI_PICO,mcu=rp2,programmer=picotool",
    relays_closed={
        EnumFut.FUT_I2C: [2, 3, 4, 5],
        EnumFut.FUT_ONEWIRE: [2, 3, 4],
    },
    mcu_config=McuConfig(
        trig1="GP20",
        trig2="GP21",
        i2c="i2c = I2C(1, scl=Pin('GP19'), sda=Pin('GP18'), freq=100_000)",
        onewire="GP14",
    ),
)


DOC_TENTACLE_DEVICE_POTPOURRY = """
FT232RL
  https://www.aliexpress.com/item/1005006445462581.html
I2C EEPROM AT24C08
  https://www.aliexpress.com/item/1005005344566156.html
1Wire Temperature Sensor DS18B20 TO-92
  https://www.aliexpress.com/item/1005004987470850.html
"""
tentacle_spec_device_potpourry = TentacleSpec(
    tentacle_type=TentacleType.TENTACLE_DEVICE_POTPOURRY,
    futs=[EnumFut.FUT_I2C, EnumFut.FUT_UART, EnumFut.FUT_ONEWIRE, EnumFut.FUT_TIMER],
    category="Micropython Board",
    label="potpourry_v1.0",
    doc=DOC_TENTACLE_DEVICE_POTPOURRY,
    tags="",
    relays_closed={
        EnumFut.FUT_I2C: [1, 2],
        EnumFut.FUT_ONEWIRE: [5],
    },
)

DOC_TENTACLE_DAQ_SALEAE = """
USB Logic Analyzer 24MHz 8 Channel
https://www.aliexpress.com/item/4000146595503.html
https://sigrok.org/wiki/Noname_Saleae_Logic_clone
"""
tentacle_spec_daq_saleae = TentacleSpec(
    tentacle_type=TentacleType.TENTACLE_DAQ_SALEAE,
    futs=[EnumFut.FUT_I2C, EnumFut.FUT_UART, EnumFut.FUT_ONEWIRE, EnumFut.FUT_TIMER],
    category="Micropython Board",
    label="daq:saleae_clone_v1.0",
    doc=DOC_TENTACLE_DAQ_SALEAE,
    tags="daq=saleae_clone",
    relays_closed={
        EnumFut.FUT_I2C: [1, 2, 3, 4],
        EnumFut.FUT_ONEWIRE: [1, 2, 3, 4],
    },
)
