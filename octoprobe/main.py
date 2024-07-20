import logging
import time

from usbhubctl.util_logging import init_logging

from octoprobe.infrastructure_tutorial.config_workplace_ch_wetzikon import (
    INFRASTRUCTURE,
)
from octoprobe.octoprobe import NTestRun

logger = logging.getLogger(__file__)


class DutPyboard:
    def __init__(self, runner: NTestRun):
        self.runner = runner


def main() -> None:
    init_logging()

    start_s = time.monotonic()
    print(INFRASTRUCTURE.description_short)

    runner = NTestRun(infrastructure=INFRASTRUCTURE)

    runner.session_powercycle_tentacles()

    runner.function_prepare_dut()
    runner.function_setup_infra()
    runner.function_setup_dut()

    runner.run()

    runner.session_teardown()
    logger.info(f"duration {time.monotonic()-start_s:0.1f}s")


if __name__ == "__main__":
    main()
