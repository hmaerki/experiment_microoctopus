from octoprobe.util_baseclasses import TentacleType

DOC_TENTACLE_PYBOARD = """
https://micropython.org/resources/PYBv11-schematics.pdf
https://micropython.org/resources/pybv11-pinout.jpg

Connections:
tentacle  | pyboard
relay 1   | BOOT0
relay 1   | 3V3
"""
tentacle_type_pyboard = TentacleType(
    category="Micropython Board",
    label="pyboard_v1.0",
    doc=DOC_TENTACLE_PYBOARD,
    tags="programmer=dfu-util",
    octobus="trigger1,trigger2,onewire,i2c,uart",
    relay_1="bootbutton",
    relay_2="onewire",
    relay_3="i2c.sda",
    relay_4="i2c.clk",
    relay_5="uart.rx",
    relay_6="uart.tx",
)

DOC_TENTACLE_SEED_PICO = """
https://files.seeedstudio.com/wiki/XIAO-RP2040/res/Seeed-Studio-XIAO-RP2040-v1.3.pdf
https://files.seeedstudio.com/wiki/XIAO-RP2040/img/xinpin.jpg

Connections:
tentacle  | pyboard
relay 1   | GND (pin2)
relay 1   | RP2040_BOOT (requires soldering)
"""
tentacle_type_seed_pico = TentacleType(
    category="Micropython Board",
    label="seeed_pico_v1.0",
    doc=DOC_TENTACLE_SEED_PICO,
    tags="programmer=picotool",
    octobus="trigger1,trigger2,onewire,i2c,uart",
    relay_1="bootbutton",
    relay_2="onewire",
    relay_3="i2c.sda",
    relay_4="i2c.clk",
    relay_5="uart.rx",
    relay_6="uart.tx",
)


DOC_TENTACLE_MULIT_DEVICES = """
FT232RL
  https://www.aliexpress.com/item/1005006445462581.html
I2C EEPROM AT24C08
  https://www.aliexpress.com/item/1005005344566156.html
1Wire Temperature Sensor DS18B20 TO-92
  https://www.aliexpress.com/item/1005004987470850.html
"""
tentacle_type_seed_pico = TentacleType(
    category="Micropython Board",
    label="multi_devices_v1.0",
    doc=DOC_TENTACLE_MULIT_DEVICES,
    tags="onewire:ds18b,i2c:AT24C08,uart:ft232",
    octobus="onewire,i2c,uart",
)

DOC_TENTACLE_SALEAE_CLONE = """
USB Logic Analyzer 24MHz 8 Channel
https://www.aliexpress.com/item/4000146595503.html
https://sigrok.org/wiki/Noname_Saleae_Logic_clone
"""
tentacle_type_seed_pico = TentacleType(
    category="Micropython Board",
    label="daq:saleae_clone_v1.0",
    doc=DOC_TENTACLE_MULIT_DEVICES,
    tags="daq_saleae_clone",
    octobus="trigger1,trigger2,onewire,i2c,uart",
)
