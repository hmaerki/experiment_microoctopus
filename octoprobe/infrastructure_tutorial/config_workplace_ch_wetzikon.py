from __future__ import annotations

from octoprobe.infrastructure_tutorial.config_tentacles import (
    tentacle_spec_daq_saleae,
    tentacle_spec_device_potpourry,
    tentacle_spec_pyboard,
    tentacle_spec_raspberry_pico,
)
from octoprobe.lib_infrastructure import Infrastructure
from octoprobe.lib_tentacle import Tentacle

tentacle_mcu_pyboard = Tentacle(
    tentacle_serial_number="e4636874db3a2333",
    tentacle_spec=tentacle_spec_pyboard,
)
tentacle_mcu_raspberry_pico = Tentacle(
    tentacle_serial_number="e4636874db1a5133",
    tentacle_spec=tentacle_spec_raspberry_pico,
)
tentacle_daq_saleae = Tentacle(
    tentacle_serial_number="e4636874db124f35",
    tentacle_spec=tentacle_spec_daq_saleae,
)
tentacle_device_potpourry = Tentacle(
    tentacle_serial_number="e4636874db405d32",
    tentacle_spec=tentacle_spec_device_potpourry,
)


INFRASTRUCTURE = Infrastructure(
    tentacles=[
        tentacle_mcu_pyboard,
        tentacle_mcu_raspberry_pico,
        tentacle_device_potpourry,
        tentacle_daq_saleae,
    ],
)
