# from __future__ import annotations

import dataclasses
from typing import Iterator
# from test_fut_uart import (
#     Tentacle,
#     TentacleType,
#     EnumFut,
# )


# def main() -> None:
#     for marker_standard in (
#         MarkerStandard(
#             required_futs=[EnumFut.FUT_UART],
#             required_device_potpourry=True,
#             optional_daq_saleae=True,
#         ),
#         MarkerStandard(
#             required_futs=[EnumFut.FUT_I2C],
#             required_device_potpourry=True,
#             optional_daq_saleae=True,
#         ),
#         MarkerStandard(
#             required_futs=[EnumFut.FUT_I2C],
#             required_device_potpourry=False,
#             required_daq=True,
#         ),
#     ):
#         list_list_tentacle = marker_standard.run_factory()
#         print(f"required_futs={marker_standard.required_futs}")
#         for run_tentacles in list_list_tentacle:
#             run = RunStandard(run_tentacles=run_tentacles)
#             print(run.short)


# if __name__ == "__main__":
#     main()
