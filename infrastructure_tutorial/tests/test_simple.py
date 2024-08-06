import pytest

from config_constants import EnumFut
from octoprobe.lib_tentacle import Tentacle


@pytest.mark.required_futs(EnumFut.FUT_I2C)
def test_i2c(
    mcu: Tentacle,
    device_potpourry: Tentacle,
    daq_saleae: Tentacle,
) -> None:
    assert mcu.dut is not None
    mp_program = """
from machine import Pin, I2C

{{mcu_config.i2c}}

pin_trigger_1 = Pin('{{mcu_config.trig1}}', mode=Pin.OUT, value=0)
pin_trigger_2 = Pin('{{mcu_config.trig2}}', mode=Pin.OUT, value=0)
pin_trigger_1.value(1)
i2c_data = i2c.readfrom(0x50, 10, True)
pin_trigger_1.value(0)
"""
    _ret = mcu.dut.mp_remote.exec_render(
        mp_program, mcu_config=mcu.tentacle_spec.mcu_config
    )

    i2c_data = mcu.dut.mp_remote.read_bytes("i2c_data")
    print(f"i2c_data: {i2c_data!r}")
    assert i2c_data == b"\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff"


@pytest.mark.required_futs(EnumFut.FUT_ONEWIRE)
def test_onewire(
    mcu: Tentacle,
    device_potpourry: Tentacle,
    daq_saleae: Tentacle,
) -> None:
    assert mcu.dut is not None

    mp_program = """
from machine import Pin
import onewire
import time
import ds18x20

ow = onewire.OneWire(Pin('{{mcu_config.onewire}}'))
ds = ds18x20.DS18X20(ow)

pin_trigger_1 = Pin('{{mcu_config.trig1}}', mode=Pin.OUT, value=0)
pin_trigger_2 = Pin('{{mcu_config.trig2}}', mode=Pin.OUT, value=0)
pin_trigger_1.value(1)
roms = ds.scan()
pin_trigger_1.value(0)

ds.convert_temp()
time.sleep_ms(750)
temperatures_c = [ds.read_temp(rom) for rom in roms]
"""
    mcu.dut.mp_remote.exec_render(mp_program, mcu_config=mcu.tentacle_spec.mcu_config)

    roms = mcu.dut.mp_remote.read_list("roms")
    print(f"roms: {roms}")

    assert (
        len(roms) == 2
    ), f"Two DS18 temperature sensors expected, but got {len(roms)}!"

    temperatures_c = mcu.dut.mp_remote.read_list("temperatures_c")
    print(f"temperatures_c: {temperatures_c}")
