# Terms

* `microOctopus`: micropyton Octopus
* `Gadget`: Something that may be collected to a micropython board: A sensor, actor, display or even a Modbus dongle.
* `DUT`: Device Under Test.
 * UUT: Unit under test
* `BoardDUT`: A micropython board under test.
* `GadgetDUT`: A gadget under test.
* `Tentacle`: microOctopus has many tentacles, every tentacle may host a DUT.
* `BoardTentacle`: A tentacle holding a micropython board.
* `GadgetTentacle`: A tentacle holding a gadget.
* `Inkbus`: All tentacles are connected by the inkbus: A 40 wire ribbon cable.

* HIL: Hardware in the loop

 * I2C Controller (master)
 * I2C Target/Peripheral (slave)
 * ATE (ex infra): the microOctopus hardware which builds the infrastructure to run the tests
 * aux hardware: Additional hardware which supports the test
 * FUT (NO): Feature under test. For example I2C code streaching.
 * TP (NO): Test participiant.
   * If the I2C code streaching should be tested, we require a *TP I2C controller* and a *TP I2C target*.
   * The DUT may now be the *TP I2C controller* or the *TP I2C target*.
   * Remember
     * TP is hardware. DUT is the role of the hardware in a test scenario.
 * Inkbus: The databus connecting tentacles. A octopus releases ink, so we call it inkbus.

* https://en.wikipedia.org/wiki/Automatic_test_equipment
  * https://en.wikipedia.org/wiki/Test_automation
  * ATE: Automatic test equipment
  * ITA: Interface Test Adapter
  * Fixture
  * Test equipment switching
  * Test equipment platforms

* https://www.trentonsystems.com/blog/automatic-test-equipment-overview
  * UUT Unit under test
  * EUT Equipment under test
