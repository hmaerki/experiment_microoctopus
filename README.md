
# microOctopus - Micropython Testenvironment

Ideas on how to set up a micropython testenvironment

![microOctopus](branding/images/uOctopus-pytest.png)

## Terms

* `microOctopus`: micropyton Octopus
* `Gadget`: Something that may be collected to a micropython board: A sensor, actor, display or even a Modbus dongle.
* `DUT`: Device Under Test.
* `BoardDUT`: A micropython board under test.
* `GadgetDUT`: A gadget under test.
* `Tentacle`: microOctopus has many tentacles, every tentacle may host a DUT.
* `BoardTentacle`: A tentacle holding a micropython board.
* `GadgetTentacle`: A tentacle holding a gadget.
* `Inkbus`: All tentacles are connected by the inkbus: A 40 wire ribbon cable.


## Goal

* `microOctopus` allows to automatically test various micropython boards against various gadgets.
* Tests should run automatically and include firmware update.
* Tests should be triggered from the github workflow, for example on commits or pull requests.

## microOctopus testenvironment

* Software:
  * dockerized on linux
  * Test script: `pytest`
  * github runner
* Hardware
  * A tentacle may be ordered assembled at JLCPCB and will cost below USD50.
  * Every tentacle is equipped by a RP2040 which controls the DUT.
  * The Inkbus connects the tentacles. Typically exactly one BoardTentacle and one GadgetTentacle is connected to the Inkbus.
* Extended Hardware
  * microOctopus may also have specialized tentacles like a scope tentacle.
  * microOctopus may also control cams to read displays, wlan hotspot, etc.
* Firmware under test
  * Must be provided by the tester
* Test software
  * microOctopus provides basic functionality like updating firmware, connecting the inkbus, tentacle inventory.
  * However the pytest code itselve is provided by the tester together with the firmware.

## Hardware example

* `microOctopus`
  * `BoardTentacle` PYBv1.1
  * `BoardTentacle` ESP32
  * `GadgetTentacle` OLED

Tentacles side by side connected by a 40 pin ribbon cable

![tentacle top all](README_images/uoctopus_tentacle_top-all.png)

Tentacles stacked

![tentacle right all](README_images/uoctopus_tentacle_right-all.png)

## Test flow

In this test the OLED display shall be tested agains PYBv1.1 and ESP32 using firmware v9.12.

```mermaid
sequenceDiagram
    participant github
    participant U as microOctopus
    participant TP as Tentacle PYBv1.1
    participant TE as Tentacle ESP32
    participant TO as Tentacle OLED
    participant I as Inkbus
    github->>U: send firmware v9.12 and testcode

    Note over U,TO: Test PYBv1.1 vs OLED

    U->>+TP: update firmware
    TP->>+I: connect to inkbus
    TO->>+I: connect to inkbus
    U->>+TP: run pytest
    TP-->>-U: collect results
    I-->>-TP: disconnect inkbus
    I-->>-TO: disconnect inkbus

    Note over U,TO: Test ESP32 vs OLED

    U->>+TE: update firmware
    TE->>+I: connect to inkbus
    TO->>+I: connect to inkbus
    U->>+TE: run pytest
    TE-->>-U: collect results
    I-->>-TE: disconnect inkbus
    I-->>-TO: disconnect inkbus

    U-->>github: testresults
```