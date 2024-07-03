import logging
import time

from usbhubctl.util_logging import init_logging

from octoprobe.config.config_infrastructure_wetzikon_a import (
    INFRASTRUCTURE,
    tentacle_pyboard,
    tentacle_seed_pico,
)
from octoprobe.octoprobe import Runner

logger = logging.getLogger(__file__)


class DutPyboard:
    def __init__(self, runner: Runner):
        self.runner = runner


def main() -> None:
    init_logging()

    start_s = time.monotonic()
    print(INFRASTRUCTURE.description_short)

    runner = Runner(
        infrastructure=INFRASTRUCTURE,
        active_tentacles=[
            tentacle_pyboard,
            tentacle_seed_pico,
        ],
    )

    runner.find_active_tentacles()

    runner.setup_infra()

    runner.setup_dut()

    runner.teardown()
    logger.info(f"duration {time.monotonic()-start_s:0.1f}s")


if __name__ == "__main__":
    main()
