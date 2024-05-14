"""
Generics:
* DUT Sucker: Micropython
* DUT Sucker: Zephyr
* DUT Sucker: FreeRTOS
* DUT Sucker: Device I2C
* DUT Sucker: Device UART
* DUT Sucker: Aquisition sigrok

* Tentacle RP2
  * How the relais are assigned
  * How the relais work (on/off, pulse, pwm)
  * What software is downloaed

Who specifies what the RP2040 on the tencacle infra does?
* Tentacle
* TentacleRP2
  * Boot
* TentacleDFUUTIL
  * Boot
  * Reset

BusI2C
  * SCL
  * SDA
  * Trigger

BusUART
  * RX
  * TX
  * Trigger

BusMODBUS
  * RX
  * TX
  * Trigger
  * Master Enable
  * Slave Enable

BusSPI

Fixtures to control the tests:
  tentacle_mcu
   * infra
   * sucker_mcu[Micropython|Zephyr]
   * bus
  tentacle_device
   * infra
   * bus
  tentacle_acquisition

"""

from typing import TypeVar

T = TypeVar("T", int, str)


def x(i: T) -> tuple[T, T]:
    return (2 * i, i + i + i)


def y(i: T) -> T:
    return 2 * i


a: str = y("y")
j: int = y(5)

print(x("x"))
print(y("y"))
