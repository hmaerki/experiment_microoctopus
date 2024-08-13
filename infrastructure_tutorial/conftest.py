import logging
import pathlib
from collections.abc import Iterator

import pytest
from pytest import fixture
from usbhubctl.util_logging import init_logging

from octoprobe.lib_tentacle import Tentacle
from octoprobe.octoprobe import NTestRun
from octoprobe.util_dut_programmers import FirmwareSpec
from octoprobe.util_pytest import break_into_debugger_on_exception

from .config_constants import EnumFut, TentacleType
from .config_workplace_ch_wetzikon_1 import INFRASTRUCTURE

logger = logging.getLogger(__file__)

DIRECTORY_OF_THIS_FILE = pathlib.Path(__file__).parent

DEFAULT_FIRMWARE_SPEC = (
    DIRECTORY_OF_THIS_FILE / "pytest_args_firmware_RPI_PICO_v1.22.1.json"
)


_PYTEST_OPT_FIRMWARE = "--firmware"

# Uncomment to following line
# to stop tests on exceptions
break_into_debugger_on_exception(globals())


def get_firmware_spec(config: pytest.Config) -> FirmwareSpec:
    assert isinstance(config, pytest.Config)

    firmware_spec_filename = config.getoption(_PYTEST_OPT_FIRMWARE)
    return FirmwareSpec.factory(filename=firmware_spec_filename)


def pytest_generate_tests(metafunc: pytest.Metafunc) -> None:
    print(metafunc.definition.nodeid)
    for marker in metafunc.definition.own_markers:
        print(f" {marker!r}")

    def get_marker(name: str) -> pytest.Mark:
        for marker in metafunc.definition.own_markers:
            if marker.name == name:
                return marker
        raise AssertionError()

    marker_required_futs = get_marker(name="required_futs")
    assert isinstance(marker_required_futs, pytest.Mark)
    _required_futs = list(marker_required_futs.args)
    assert isinstance(_required_futs, list)
    for fut in _required_futs:
        assert EnumFut(fut), fut

    if "mcu" in metafunc.fixturenames:
        tentacles = TentacleType.TENTACLE_MCU.get_tentacles_for_type(
            tentacles=INFRASTRUCTURE.tentacles,
            required_futs=_required_futs,
        )
        firmware_spec = get_firmware_spec(config=metafunc.config)
        tentacles = list(filter(firmware_spec.match_board, tentacles))
        assert len(tentacles) > 0

        def get_id(t: Tentacle) -> str:
            return t.pytest_id

        metafunc.parametrize("mcu", tentacles, ids=get_id)

    if "device_potpourry" in metafunc.fixturenames:
        tentacles = TentacleType.TENTACLE_DEVICE_POTPOURRY.get_tentacles_for_type(
            INFRASTRUCTURE.tentacles,
            required_futs=_required_futs,
        )
        assert len(tentacles) > 0
        metafunc.parametrize("device_potpourry", tentacles, ids=lambda t: t.pytest_id)

    if "daq_saleae" in metafunc.fixturenames:
        tentacles = TentacleType.TENTACLE_DAQ_SALEAE.get_tentacles_for_type(
            INFRASTRUCTURE.tentacles,
            required_futs=_required_futs,
        )
        assert len(tentacles) > 0
        metafunc.parametrize("daq_saleae", tentacles, ids=lambda t: t.pytest_id)


@pytest.fixture
def required_futs(request: pytest.FixtureRequest) -> tuple[EnumFut]:
    for m in request.node.own_markers:
        assert isinstance(m, pytest.Mark)
        if m.name == "required_futs":
            return m.args
    raise AssertionError()


@pytest.fixture
def active_tentacles(request: pytest.FixtureRequest) -> list[Tentacle]:
    def inner() -> Iterator[Tentacle]:
        for _param_name, param_value in request.node.callspec.params.items():
            if isinstance(param_value, Tentacle):
                yield param_value

    return list(inner())


@fixture(scope="session", autouse=True)
def testrun(request: pytest.FixtureRequest) -> Iterator[NTestRun]:
    init_logging()
    firmware_spec = get_firmware_spec(request.config)
    firmware_spec.download()
    _testrun = NTestRun(
        infrastructure=INFRASTRUCTURE,
        firmware_spec=firmware_spec,
    )

    _testrun.session_powercycle_tentacles()

    yield _testrun

    _testrun.session_teardown()


@fixture(scope="function", autouse=True)
def setup_tentacles(
    testrun: NTestRun,  # pylint: disable=W0621:redefined-outer-name
    required_futs: tuple[EnumFut],  # pylint: disable=W0621:redefined-outer-name
    active_tentacles: list[Tentacle],  # pylint: disable=W0621:redefined-outer-name
) -> Iterator[None]:
    try:
        testrun.function_prepare_dut()
        testrun.function_setup_infra()
        testrun.function_setup_dut(active_tentacles=active_tentacles)

        testrun.setup_relays(futs=required_futs, tentacles=active_tentacles)

        yield

    finally:
        try:
            testrun.function_teardown(active_tentacles=active_tentacles)
        except Exception as e:
            logger.exception(e)


@fixture
def global_fixture() -> None:
    print("\n(Doing global fixture setup stuff!)")


def pytest_addoption(parser: pytest.Parser) -> None:
    parser.addoption(
        _PYTEST_OPT_FIRMWARE,
        action="store",
        default=str(DEFAULT_FIRMWARE_SPEC),
        help="A json file specifying the firmware",
    )
