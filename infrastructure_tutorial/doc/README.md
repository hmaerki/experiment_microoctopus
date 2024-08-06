# Infrastructure `INFRASTRUCTURE_TUTORIAL`

Every infrastructure requires a unique label. This is `INFRASTRUCTURE_TUTORIAL`.

Other infrastructure labels could be:
* `INFRASTRUCTURE_MODBUS`: Modbus RTU is very time critical, specially timeouts/retires. This infrastructure tests these timing aspects, specially in error and race condition.
* `INFRASTRUCTURE_I2C_MULTCONTROLLER`: In multicontroller (multimaster) mode many special situations an race condition may occur. The infrastructure provides the hardware to create error conditions like shortening the bus. It may be tested if and how the software recovers from these errors.
* ...

This infrastructure demonstrates the various aspects of octoprobe.

It allows to write/run meaningful tests.

Another aspect is how the documention/specification of the infrastructure and tentacles relate.

## How to use this specification / rationale

* Define **signal_labels**: These labels have to be used in
  * tentacle schematics
  * test source code
  * Example `SIGNAL_DATA1`

* Define **fut_labels** (`FUT`: Feature Under Test):
  * These labels have to be used in
    * tentacle configuration
    * test code markers
  * Example `FUT_I2C`

* Define **tentacle_role**: These labels have to be used in
  * tentacle configuration
  * Example `TENTACLE_MCU_xxx`/`TENTACLE_DEVICE_xxx`

Define what may be tested with this infrastructure.

Define how test must be written to be able to run on this infrastructure.

# Specification `INFRASTRUCTURE_TUTORIAL`

## Octobus

`Octobus` is the 40pin ribbon wire cable which connects the tentacles.

| Pin | signal_label | `FUT_I2C` | `FUT_UART` | `FUT_ONEWIRE` | Comment |
| - | - | - | - | - | - |
| 5 | `SIGNAL_TRIGGER1` | - | trigger | - | logic analyzer, measures delays |
| 7 | GND |
| 9 | `SIGNAL_TRIGGER2` | - | trigger | - | logic analyzer, measures delays |
| 11 | GND |
| 13 | `SIGNAL_DATA1` | SCL | TX | data |
| 15 | GND |
| 17 | `SIGNAL_DATA2` | SDA | RX | - |
| 19 | GND |

All signals are 3.3V.

Why are the `SIGNAL_DATA1/2` lines shared for different protocols? The current tentacles only provide limited relays, so only a few data lines may be controlled.

Tentacle roles

| Tentacle role | Comment |
| - | - |
| `TENTACLE_MCU` | A microprocessor tentacle |
| `TENTACLE_DEVICE_POTPOURRY` | A tentacle with several devices |
| `TENTACLE_DAQ_SALEAE` | Dataaquisition and error provoking |



## Feature under test `FUT_TIMER`.

* Test proposals
  * Clock dividers, timers
    * stimuly: `TENTACLE_MCU` generates pulse or PWM on `SIGNAL_TRIGGER1/2`.
    * expected: `TENTACLE_DAQ_SALEAE` verifies this pulse.


## Feature under test `FUT_I2C`.

* Electrical setup
  * Exacly one `TENTACLE_MCU` connects to `SIGNAL_DATA1/2`.
  * Exactly one `TENTACLE_DEVICE_POTPOURRY` connects to `SIGNAL_DATA1/2`. This tentacle must provide the I2C pull ups.

* Test proposals
  * Datatransfer
    * stimuly: `TENTACLE_MCU` acts as a I2C-controller and the `TENTACLE_DEVICE_POTPOURRY` as a I2C-target.
    * expected: meaningful data
  * Errors
    * See comments below


## Feature under test `FUT_UART`.

* Electrical setup
  * Exacly one `TENTACLE_MCU` connects to `SIGNAL_DATA1/2` and `SIGNAL_TRIGGER1/2`.
    * The TX pin of `TENTACLE_MCU` / `TENTACLE_DEVICE_POTPOURRY` requires a serial 1k resistor. This allows the `TENTACLE_DAQ_SALEAE` to destroy the signal.
  * Exactly one `TENTACLE_DEVICE_POTPOURRY` connects to `SIGNAL_DATA1/2`.

* Test proposals
  * Timing test sequence:
    * stimuly:
      * `TENTACLE_MCU`: `SIGNAL_TRIGGER1` low->high
      * `TENTACLE_MCU`: `SIGNAL_DATA1` send 3 characters
      * `TENTACLE_MCU`: `SIGNAL_TRIGGER1` high->low
    * expected:
      * This tests allows various timing aspects. For example [uart.flush()](https://github.com/micropython/micropython/issues/13377)
    * variants:
      * Test hardware UART vs software UART.
      * Test syncio vs asyncio.
  * Errors
    * See comments below

## Feature under test `FUT_ONEWIRE`.

* Electrical setup
  * Exacly one `TENTACLE_MCU` connects to `SIGNAL_DATA1`.
  * Exactly one `TENTACLE_DEVICE_POTPOURRY` connects to `SIGNAL_DATA1`. This tentacle must provide the onewire pull up.

* Test proposals
  * OneWire scan without response
    * stimuly: `TENTACLE_MCU`: scan for sensors. No sensor is connected by opening the ONEWIRE relay and closing the I2C-SCL relay.
    * expected: No response after some timeout.
  * OneWire scan
    * stimuly: `TENTACLE_MCU`: scan for sensors.
    * expected: 2 sensors found.
  * OneWire communication
    * stimuly: `TENTACLE_MCU`: reads serial number from one sensors.
    * expected: serial number
  * OneWire communication with error
    * See comments below

## Feature under test `FUT_I2C/FUT_UART/FUT_ONEWIRE`: Communication errors.

* Test proposals
  * Recovering from errors
    * stimuly: I2C/UART/ONEWIRE communication. Now `TENTACLE_DAQ_SALEAE` tentacle overrides `SIGNAL_DATA1/2` to provoke errors.
    * expected: Error and recover.
    * challenge
      * How to introduce errors without introducing flakyness?
      * How to provoke data integrity errors (CRC)?
      * How to provoke protocol errors (timeouts, start/stop bit missing)?

How to electrically override `SIGNAL_DATA1/2`:
  * I2C/ONEWIRE: `SIGNAL_DATA1/2` are pulled up. `TENTACLE_DAQ_SALEAE` may just override these outputs.
  * UART: The TX-signals outputs have low impedance. A serial 1k resitor is added (see `TENTACLE_MCU_x`/`TENTACLE_DEVICE_x`) which then allows `TENTACLE_DAQ_SALEAE` to override both TX-signals.

# Impelmentation `INFRASTRUCTURE_TUTORIAL`

[Schematics](schematics_kicad/schematics.pdf)

## Implementation `TENTACLE_MCU_GROBOTICS_PYBAORD`

[README.md](tentacle_MCU_grobotics_pyboard/README.md)

## Implementation `TENTACLE_MCU_RASPBERRY_PICO`

[README.md](tentacle_MCU_raspberry_pico/README.md)

## Implementation `TENTACLE_DEVICE_POTPOURRY`

[README.md](tentacle_DEVICE_potpourri/README.md)

## Implementation `TENTACLE_DAQ_SALEAE`

[README.md](tentacle_DAQ_saleae/README.md)
