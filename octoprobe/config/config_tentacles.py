from octoprobe.lib_tentacle import TentacleType

"""
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
    tags="programmer=dfu-util",
    octobus="onewire,i2c,uart",
    relay_1="bootbutton",
    relay_2="onewire",
    relay_3="i2c.sda",
    relay_4="i2c.clk",
    relay_5="uart.rx",
    relay_6="uart.tx",
)

"""
https://files.seeedstudio.com/wiki/XIAO-RP2040/res/Seeed-Studio-XIAO-RP2040-v1.3.pdf
https://files.seeedstudio.com/wiki/XIAO-RP2040/img/xinpin.jpg

Connections:
tentacle  | pyboard
relay 1   | GND (pin2)
relay 1   | RP2040_BOOT (requires soldering)
"""
tentacle_type_seed_pico = TentacleType(
    category="Micropython Board",
    label="seed_pico_v1.0",
    tags="programmer=picotool",
    octobus="onewire,i2c,uart",
    relay_1="bootbutton",
    relay_2="onewire",
    relay_3="i2c.sda",
    relay_4="i2c.clk",
    relay_5="uart.rx",
    relay_6="uart.tx",
)
