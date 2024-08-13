from __future__ import annotations

from infrastructure_tutorial.config_constants import EnumFut, TentacleType
from octoprobe.lib_infrastructure import Infrastructure
from octoprobe.lib_tentacle import Tentacle

from .config_tentacles import (
    McuConfig,
    tentacle_spec_daq_saleae,
    tentacle_spec_device_potpourry,
    tentacle_spec_pyboard,
    tentacle_spec_raspberry_pico,
)

tentacle_mcu_pyboard = Tentacle[McuConfig, TentacleType, EnumFut](
    tentacle_serial_number="e4636874db3a2333",
    tentacle_spec=tentacle_spec_pyboard,
)
tentacle_mcu_raspberry_pico = Tentacle[McuConfig, TentacleType, EnumFut](
    tentacle_serial_number="e4636874db1a5133",
    tentacle_spec=tentacle_spec_raspberry_pico,
)
tentacle_daq_saleae = Tentacle[McuConfig, TentacleType, EnumFut](
    tentacle_serial_number="e4636874db124f35",
    tentacle_spec=tentacle_spec_daq_saleae,
)
tentacle_device_potpourry = Tentacle[McuConfig, TentacleType, EnumFut](
    tentacle_serial_number="e4636874db405d32",
    tentacle_spec=tentacle_spec_device_potpourry,
)


INFRASTRUCTURE = Infrastructure(
    workspace="ch_wetzikon_1",
    tentacles=[
        tentacle_mcu_pyboard,
        tentacle_mcu_raspberry_pico,
        tentacle_device_potpourry,
        tentacle_daq_saleae,
    ],
)
