from __future__ import annotations

from octoprobe.infrastructure_tutorial.config_tentacles import (
    tentacle_spec_daq_saleae,
    tentacle_spec_device_potpourry,
    tentacle_spec_pyboard,
    tentacle_spec_raspberry_pico,
)
from octoprobe.lib_infrastructure import Infrastructure
from octoprobe.lib_tentacle import Tentacle
from octoprobe.util_dut_programmers import FirmwareSpec

from ..util_constants import DIRECTORY_DOWNLOADS


tentacle_mcu_pyboard = Tentacle(
    tentacle_serial_number="e4636874db3a2333",
    tentacle_spec=tentacle_spec_pyboard,
    firmware_spec=FirmwareSpec(
        # filename=DIRECTORY_DOWNLOADS / "PYBV11-20230426-v1.20.0.dfu",
        # micropython_version_text="3.4.0; MicroPython v1.20.0 on 2023-04-26",
        filename=DIRECTORY_DOWNLOADS
        / "PYBV11-20240723-v1.24.0-preview.130.ge1ecc232d.dfu",
        micropython_version_text="3.4.0; MicroPython v1.24.0-preview.130.ge1ecc232d on 2024-07-23",
    ),
)
tentacle_mcu_raspberry_pico = Tentacle(
    tentacle_serial_number="e4636874db1a5133",
    tentacle_spec=tentacle_spec_raspberry_pico,
    firmware_spec=FirmwareSpec(
        filename=DIRECTORY_DOWNLOADS / "RPI_PICO-20231005-v1.21.0.uf2",
        micropython_version_text="3.4.0; MicroPython v1.22.2 on 2024-02-22",
    ),
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
