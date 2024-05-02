# Configurations

## USB Hub Models

* Configuration required to detect hub
* Mapping from bus/port to port id

## Tentacles Types

```python
TentacleType(
    category="Micropython Board"
    label="pyboard_v1.0"
    tags="programming=dfu-util"
    octobus="onewire,i2c,uart"
    relay_1="bootbutton"
    relay_2="onewire"
    relay_3="i2c.sda"
    relay_4="i2c.clk"
    relay_5="uart.rx"
    relay_6="uart.tx"
)
TentacleType(
    category="Micropython Board"
    label="esp32_v1.0"
    tags="programming=esptool.py"
    octobus="onewire,i2c,uart"
    relay_1="bootbutton"
    relay_2="onewire"
    relay_3="i2c.sda"
    relay_4="i2c.clk"
    relay_5="uart.rx"
    relay_6="uart.tx"
)
```

## Tentacles Inventory

```python
Tentacle(
    serial="1234"
    type="pyboard_v1.0"
)
Tentacle(
    serial="1235"
    type="esp32_v1.0"
)
Tentacle(
    # https://github.com/micropython/micropython-lib/tree/master/micropython/drivers/sensor/ds18x20
    serial="1236"
    category="device"
    octobus="onewire"
    tags="device=ds18x20"
)
Tentacle(
    serial="1237"
    category="daq"
    octobus="onewire,i2c,uart"
    tags="daq=saleae_generic"
)
```

## USB Hubs attached, Tentacles connected

* Just a list ob hubs

```python
UsbHub(
    model="RHT107A"
    port1="1234",
    port3="1235",
    port4="1236",
    port5="1237",
)
```