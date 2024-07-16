from __future__ import annotations

import enum
from dataclasses import dataclass
import itertools

import pytest


class TentacleType(enum.StrEnum):
    TENTACLE_MCU = enum.auto()
    TENTACLE_DEVICE = enum.auto()
    TENTACLE_DAQ = enum.auto()


class EnumFut(enum.StrEnum):
    FUT_I2C = enum.auto()
    FUT_UART = enum.auto()
    FUT_TIMER = enum.auto()


@dataclass
class Tentacle:
    tag: str
    tentacle_type: TentacleType
    futs: list[EnumFut]

    def has_required_futs(self, required_futs: list[EnumFut]) -> bool:
        for required_fut in required_futs:
            if required_fut in self.futs:
                return True
        return False


@dataclass
class Infrastructure:
    tentacles: list[Tentacle]

    def get_tentacles_for_type(
        self, tentacle_type: TentacleType, required_futs: list[EnumFut]
    ) -> list[Tentacle]:
        list_tentacles = []
        for tentacle in self.tentacles:
            if tentacle.tentacle_type is tentacle_type:
                if tentacle.has_required_futs(required_futs=required_futs):
                    list_tentacles.append(tentacle)
        return list_tentacles

    def select_tentacles(self, required: Required) -> list[list[Tentacle]]:
        list_selected = []
        for r in required.tentacle_types:
            tentacles = self.get_tentacles_for_type(
                tentacle_type=r,
                required_futs=required.fut_types,
            )
            list_selected.append(tentacles)
        return list_selected


@dataclass
class Required:
    tentacle_types: list[TentacleType]
    fut_types: list[EnumFut]


INFRASTRUCTURE = Infrastructure(
    tentacles=[
        Tentacle(
            tag="TENTACLE_MCU_RP2",
            tentacle_type=TentacleType.TENTACLE_MCU,
            futs=[EnumFut.FUT_I2C, EnumFut.FUT_UART],
        ),
        Tentacle(
            tag="TENTACLE_MCU_PYBAORD",
            tentacle_type=TentacleType.TENTACLE_MCU,
            futs=[
                EnumFut.FUT_I2C,
            ],
        ),
        Tentacle(
            tag="TENTACLE_MCU_ESP32",
            tentacle_type=TentacleType.TENTACLE_MCU,
            futs=[EnumFut.FUT_UART],
        ),
        Tentacle(
            tag="TENTACLE_DEVICE_POTPOURRY",
            tentacle_type=TentacleType.TENTACLE_DEVICE,
            futs=[EnumFut.FUT_I2C, EnumFut.FUT_UART],
        ),
        Tentacle(
            tag="TENTACLE_DEVICE_I2C",
            tentacle_type=TentacleType.TENTACLE_DEVICE,
            futs=[EnumFut.FUT_I2C],
        ),
        Tentacle(
            tag="TENTACLE_DEVICE_UART",
            tentacle_type=TentacleType.TENTACLE_DEVICE,
            futs=[EnumFut.FUT_UART],
        ),
        Tentacle(
            tag="TENTACLE_DAQ_SALEAE",
            tentacle_type=TentacleType.TENTACLE_DAQ,
            futs=[EnumFut.FUT_I2C, EnumFut.FUT_UART],
        ),
    ]
)


@dataclass
class ParameterTentacles:
    """
    This returns the tentacles to be used in this test.
    And also other test parameters like syncio/asynio.
    """

    required: Required
    tentacles: list[TentacleType]
    identifier_note: str = None
    smoke: bool = False

    def __post_init__(self):
        """
        You may check for correct datatypes here.
        Or use pydantic which does this for you.
        """
        assert isinstance(self.identifier_note, type(None) | str)
        assert isinstance(self.smoke, bool)

    @property
    def identifier(self) -> str:
        """
        This will be the paramter [...] used by pytest.
        """
        # tentacles_text = ",".join(sorted([t.tag for t in self.tentacles]))
        tentacles_text = f"{self.tentacle_mcu.tag},{self.tentacle_device.tag}"
        ident = f"{tentacles_text}"
        if self.identifier_note is not None:
            ident += self.identifier_note
        if self.smoke:
            ident += "(smoke)"
        return ident

    @classmethod
    def add_marker(cls, list_parameters) -> list:
        """
        The list of parameters is wrapped with 'pytest.param' which
        allows to add markers and the id.
        """
        for parameter in list_parameters:
            assert isinstance(parameter, cls)
            yield pytest.param(
                parameter,
                marks=pytest.mark.smoke if parameter.smoke else (),
                id=parameter.identifier,
            )

    def _get_tentacle_by_type(self, tentacle_type: TentacleType) -> Tentacle:
        pos = self.required.tentacle_types.index(tentacle_type)
        assert 0 <= pos < len(self.required.tentacle_types)
        return self.tentacles[pos]

    @property
    def tentacle_mcu(self) -> Tentacle:
        return self._get_tentacle_by_type(TentacleType.TENTACLE_MCU)

    @property
    def tentacle_device(self) -> Tentacle:
        return self._get_tentacle_by_type(TentacleType.TENTACLE_DEVICE)

    @property
    def tentacle_daq(self) -> Tentacle:
        return self._get_tentacle_by_type(TentacleType.TENTACLE_DAQ)


def pytest_generate_tests(metafunc) -> None:
    if "param" in metafunc.fixturenames:
        # Generate test cases based on the user_roles list
        def get_marker(name: str):
            for marker in metafunc.definition.own_markers:
                if marker.name == name:
                    return marker
            assert False

        marker_required_tentacles = get_marker(name="required_tentacles")
        tentacle_types = marker_required_tentacles.kwargs["tentacle_types"]
        assert isinstance(tentacle_types, list)

        marker_required_futs = get_marker(name="required_futs")
        futs_types = marker_required_futs.kwargs["fut_types"]
        assert isinstance(futs_types, list)
        required = Required(tentacle_types=tentacle_types, fut_types=futs_types)

        list_tentacles_selected = INFRASTRUCTURE.select_tentacles(required=required)

        list_list_tentacles = itertools.product(*list_tentacles_selected)
        list_test_runs = []
        for tentacles in list_list_tentacles:
            list_test_runs.append(
                # TestRun(required=REQUIRED, tentacles=test_run),
                ParameterTentacles(
                    required=required,
                    tentacles=tentacles,
                )
            )

        metafunc.parametrize("param", ParameterTentacles.add_marker(list_test_runs))


@pytest.mark.required_tentacles(
    tentacle_types=[
        TentacleType.TENTACLE_MCU,
        TentacleType.TENTACLE_DEVICE,
        TentacleType.TENTACLE_DAQ,
    ]
)
@pytest.mark.required_futs(fut_types=[EnumFut.FUT_UART])
def test_uart(param: ParameterTentacles) -> None:
    if "TENTACLE_MCU_RP2" in param.tentacle_mcu.tag:
        pytest.skip("mcu not supported")
    print(param.tentacle_mcu.tag)


@pytest.mark.required_tentacles(
    tentacle_types=[
        TentacleType.TENTACLE_MCU,
        TentacleType.TENTACLE_DEVICE,
        TentacleType.TENTACLE_DAQ,
    ]
)
@pytest.mark.required_futs(fut_types=[EnumFut.FUT_I2C])
def test_i2c(param: ParameterTentacles) -> None:
    if "TENTACLE_MCU_RP2" in param.tentacle_mcu.tag:
        pytest.skip("mcu not supported")
    print(param.tentacle_mcu.tag)
