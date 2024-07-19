from __future__ import annotations

import enum
from dataclasses import dataclass
import itertools
from typing import cast

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

    @property
    def short(self) -> str:
        return self.tag.replace("TENTACLE_", "")


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
    tentacles: tuple[Tentacle]
    identifier_note: str | None = None
    smoke: bool = False

    def __post_init__(self) -> None:
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
        tentacles_text = ",".join(sorted([t.short for t in self.tentacles]))
        # tentacles_text = f"{self.tentacle_mcu.tag},{self.tentacle_device.tag}"
        ident = f"{tentacles_text}"
        if self.identifier_note is not None:
            ident += self.identifier_note
        if self.smoke:
            ident += "(smoke)"
        return ident

    @classmethod
    def add_marker(cls, list_parameters: list[ParameterTentacles]) -> list:
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


def pytest_generate_tests(metafunc: pytest.Metafunc) -> None:
    if "param2" in metafunc.fixturenames:
        # Generate test cases based on the user_roles list

        print(metafunc.definition.nodeid)
        for marker in metafunc.definition.own_markers:
            print(f" {marker!r}")

        def get_marker(name: str) -> pytest.Mark:
            for marker in metafunc.definition.own_markers:
                if marker.name == name:
                    return marker
            assert False

        marker_required = get_marker(name="required")
        required = marker_required.kwargs["required"]
        assert isinstance(required, Required)

        list_tentacles_selected = INFRASTRUCTURE.select_tentacles(required=required)

        list_list_tentacles = itertools.product(*list_tentacles_selected)
        list_test_runs: list[ParameterTentacles] = []
        for tentacles in list_list_tentacles:
            list_test_runs.append(
                # TestRun(required=REQUIRED, tentacles=test_run),
                ParameterTentacles(
                    required=required,
                    tentacles=cast(tuple[Tentacle], tentacles),
                )
            )

        metafunc.parametrize("param2", ParameterTentacles.add_marker(list_test_runs))


@pytest.mark.required(required=
    Required(
        tentacle_types=[
            TentacleType.TENTACLE_MCU,
            TentacleType.TENTACLE_DEVICE,
            TentacleType.TENTACLE_DAQ,
        ],
        fut_types=[EnumFut.FUT_UART],
    )
)
def test_uart(param2: ParameterTentacles) -> None:
    if "TENTACLE_MCU_RP2" in param2.tentacle_mcu.tag:
        pytest.skip("mcu not supported")
    print(param2.tentacle_mcu.tag)


@pytest.mark.required(required=
    Required(
        tentacle_types=[
            TentacleType.TENTACLE_MCU,
            TentacleType.TENTACLE_DEVICE,
            TentacleType.TENTACLE_DAQ,
        ],
        fut_types=[EnumFut.FUT_I2C],
    )
)
def test_i2c(param2: ParameterTentacles) -> None:
    if "TENTACLE_MCU_RP2" in param2.tentacle_mcu.tag:
        pytest.skip("mcu not supported")
    print(param2.tentacle_mcu.tag)


class TestPotpourry:
    @pytest.mark.required(required=
        Required(
            tentacle_types=[
                TentacleType.TENTACLE_MCU,
                TentacleType.TENTACLE_DEVICE,
            ],
            fut_types=[EnumFut.FUT_UART],
        )
    )
    def test_uart(self, param2: ParameterTentacles) -> None:
        pass

    @pytest.mark.required(required=
        Required(
            tentacle_types=[
                TentacleType.TENTACLE_MCU,
                TentacleType.TENTACLE_DEVICE,
            ],
            fut_types=[EnumFut.FUT_I2C],
        )
    )
    def test_i2c(self, param2: ParameterTentacles) -> None:
        pass
