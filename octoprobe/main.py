import time
import logging

from octoprobe.config.config_infrastructure_wetzikon_a import (
    INFRASTRUCTURE,
    tentacle_pyboard,
    tentacle_seed_pico,
)
from octoprobe.octoprobe import Runner

from usbhubctl.util_logging import init_logging

logger = logging.getLogger(__file__)


class DutPyboard:
    def __init__(self, runner: Runner):
        self.runner = runner


def main():
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

    runner.reset_infa_dut()

    runner.setup_infra()

    runner.setup_dut()

    runner.teardown()
    logger.info(f"duration {time.monotonic()-start_s:0.1f}s")


if __name__ == "__main__":
    main()
