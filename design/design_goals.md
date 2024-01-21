**Review**

# Goals to archive with microOctopus

*Start small, then grow.* This page is about *start small*
Terms
 * `Small`: What we slected to start with
 * `Later`: What comes after small
 * `Vision`: Long term goals.
 * `Nongoal`: What we do not want to achieve

## High level

* Vision: Offload a small selected group of micropython developers from manual testing work
* Vision: Run fully automated tests on selected set of firmware/libraries.
* Vision: Flexibility that anyone may use microOctopus and adapt it.
* Vision: Ability to write simple HIL tests which are easy to understand and maintain.
* Vision: microOctopus is about software testing - HIL. It is NOT hardware testing.
* Nongoal: Specialized hardware testing. For example USB, high speed I2C, I2S, SPI, uart.
* Nongoal: Low level entry. To set up octopus will always require some work and money.


## Define `Small`

* Selected group of developers (Just examples, lets get concrete on this list SOON)
  * SMALL: hmaerki
   * Task: Run existing tests in github/micropython/tests.
   * Goal: Bring up microOctopus
  * SMALL: hmaerki: Read/write a I2C MUX
   * Task: Start a new testframework
   * Goal: Reference test framework for microOctopus
  * Core developer X, Y, Z (lets get concrete on this SOON):
   * Task: Remote access to microOctopus @hmaerki. Run tests, write tests.
   * Goal: Feedback loop

* Selected small group of firmware/libraries are:
  * SMALL: micropython firmware an pyboard, esp32, rp2040
    * goal: firmware updates, install 'blink led' test software
    * godfather: leech, 
  * SMALL: sensors on 1wire, I2C, SPI
    * goal: use the incbus to connect the sensors
    * godfather: ...
  * LATER: complexer I2C: slave, code streching
    * godfather: hinch
  * LATER: test coverage of the whoe I2C interface.
    * godfather: ...
  * LATER: hmaerki: https://github.com/brainelectronics/micropython-modbus
    * Task: Write new tests for modbus RTU sync/asyncio. Different baud rates
    * Goal: Demonstrate how to increase code coverage.

  * Nongoal: gitlab runner, ci integration
  * Nongoal: complex gadget tentacles (scope, cams)
  * Nongoal: complex protocols (wlan, ethernet)

* Expected result
  * microOctopus up and running with 6 tentacles
  * microOctopus may be build and set up by others: Hardware (kicad/jlcpcb.com) and software available. Minimal documentation.
