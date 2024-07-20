from __future__ import annotations

import dataclasses
import enum
from dataclasses import dataclass
import itertools
from typing import Iterator, cast

import pytest


class TentacleType(enum.StrEnum):
    TENTACLE_MCU = enum.auto()
    TENTACLE_DEVICE_POTPOURRY = enum.auto()
    TENTACLE_DAQ_SALEAE = enum.auto()


class EnumFut(enum.StrEnum):
    FUT_I2C = enum.auto()
    FUT_UART = enum.auto()
    FUT_TIMER = enum.auto()


@dataclasses.dataclass
class RunTentacles:
    """
    The tentacles required for a testrun
    """

    tentacles: list[Tentacle] = dataclasses.field(default_factory=list)

    def append(self, tentacle: Tentacle) -> None:
        self.tentacles.append(tentacle)

    def pop(
        self,
        tentacle_type: TentacleType,
        optional: bool = False,
    ) -> Tentacle | None:
        for i, tentacle in enumerate(self.tentacles):
            if tentacle.tentacle_type is tentacle_type:
                del self.tentacles[i]
                return tentacle
        if optional:
            return None
        assert False

    def assert_empty(self) -> None:
        assert len(self.tentacles) == 0


@dataclasses.dataclass
class Combinations:
    tentacles: list[Tentacle]
    required_futs: list[EnumFut]
    tentacle_types: list[TentacleType]
    optional_tentacle_types: list[TentacleType]

    def get_tentacles_for_type(
        self,
        tentacle_type: TentacleType,
    ) -> list[Tentacle]:
        list_tentacles = []
        for tentacle in self.tentacles:
            if tentacle.tentacle_type is tentacle_type:
                if tentacle.has_required_futs(required_futs=self.required_futs):
                    list_tentacles.append(tentacle)
        return list_tentacles

    def combination_with_optional_tentacles(self) -> Iterator[RunTentacles]:
        for run_tentacles in self._combinations(
            tentacle_types=self.tentacle_types,
        ):
            for optional_tentacle_type in self.optional_tentacle_types:
                tentacles = self.get_tentacles_for_type(
                    tentacle_type=optional_tentacle_type,
                )
                for tentacle in tentacles:
                    run_tentacles.append(tentacle=tentacle)
            yield run_tentacles

    def _combinations(
        self, tentacle_types: list[TentacleType]
    ) -> Iterator[RunTentacles]:
        tentacle_type = tentacle_types[0]
        tentacles = self.get_tentacles_for_type(tentacle_type=tentacle_type)
        if len(tentacle_types) > 1:
            for tentacle in tentacles:
                assert tentacle.tentacle_type is tentacle_type
                for run_tentacles in self._combinations(
                    tentacle_types=tentacle_types[1:],
                ):
                    run_tentacles.append(tentacle=tentacle)
                    yield run_tentacles
            return

        for tentacle in tentacles:
            assert tentacle.tentacle_type is tentacle_type
            run_tentacles = RunTentacles()
            run_tentacles.append(tentacle)
            yield run_tentacles


@dataclass(repr=True)
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


@dataclasses.dataclass(repr=True)
class MarkerStandard:
    required_futs: list[EnumFut]
    required_device_potpourry: bool = False
    required_daq: bool = False
    optional_daq_saleae: bool = False

    def run_factory(self) -> Iterator[RunTentacles]:
        def get_tentacle_types() -> Iterator[TentacleType]:
            yield TentacleType.TENTACLE_MCU
            if self.required_device_potpourry:
                yield TentacleType.TENTACLE_DEVICE_POTPOURRY
            if self.required_daq:
                yield TentacleType.TENTACLE_DAQ_SALEAE

        def get_optional_tentacle_types() -> Iterator[TentacleType]:
            if self.optional_daq_saleae:
                yield TentacleType.TENTACLE_DAQ_SALEAE

        c = Combinations(
            tentacles=INFRASTRUCTURE.tentacles,
            required_futs=self.required_futs,
            tentacle_types=list(get_tentacle_types()),
            optional_tentacle_types=list(get_optional_tentacle_types()),
        )
        yield from c.combination_with_optional_tentacles()


class RunStandard:
    def __init__(self, run_tentacles: RunTentacles) -> None:
        assert isinstance(run_tentacles, RunTentacles)
        self.mcu = run_tentacles.pop(tentacle_type=TentacleType.TENTACLE_MCU)
        self.device_potpourry = run_tentacles.pop(
            tentacle_type=TentacleType.TENTACLE_DEVICE_POTPOURRY,
            optional=True,
        )
        self.daq_saleae = run_tentacles.pop(
            tentacle_type=TentacleType.TENTACLE_DAQ_SALEAE,
            optional=True,
        )
        run_tentacles.assert_empty()

    @classmethod
    def add_marker(
        cls,
        list_parameters: list[ParameterTentacles],
    ) -> Iterator[pytest.ParameterSet]:
        """
        The list of parameters is wrapped with 'pytest.param' which
        allows to add markers and the id.
        """
        for parameter in list_parameters:
            assert isinstance(parameter, cls)
            yield pytest.param(
                parameter,
                # marks=pytest.mark.smoke if parameter.smoke else (),
                id=parameter.identifier,
            )

    @property
    def identifier(self) -> str:
        """
        This will be the paramter [...] used by pytest.
        """
        if False:
            tentacles_text = ",".join(sorted([t.short for t in self.tentacles]))
            # tentacles_text = f"{self.tentacle_mcu.tag},{self.tentacle_device.tag}"
            ident = f"{tentacles_text}"
            if self.identifier_note is not None:
                ident += self.identifier_note
            if self.smoke:
                ident += "(smoke)"
            return ident
        return self.short

    @property
    def tentacles(self) -> Iterator[Tentacle]:
        if self.mcu is not None:
            yield self.mcu
        if self.device_potpourry is not None:
            yield self.device_potpourry
        if self.daq_saleae is not None:
            yield self.daq_saleae

    @property
    def short(self) -> str:
        return ", ".join([t.short for t in self.tentacles])


@dataclass
class Infrastructure:
    tentacles: list[Tentacle]

    def get_tentacles_for_type(
        self,
        tentacle_type: TentacleType,
        required_futs: list[EnumFut],
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
            futs=[EnumFut.FUT_I2C],
        ),
        Tentacle(
            tag="TENTACLE_MCU_ESP32",
            tentacle_type=TentacleType.TENTACLE_MCU,
            futs=[EnumFut.FUT_UART],
        ),
        Tentacle(
            tag="TENTACLE_DEVICE_POTPOURRY",
            tentacle_type=TentacleType.TENTACLE_DEVICE_POTPOURRY,
            futs=[EnumFut.FUT_I2C, EnumFut.FUT_UART],
        ),
        Tentacle(
            tag="TENTACLE_DEVICE_I2C",
            tentacle_type=TentacleType.TENTACLE_DEVICE_POTPOURRY,
            futs=[EnumFut.FUT_I2C],
        ),
        Tentacle(
            tag="TENTACLE_DEVICE_UART",
            tentacle_type=TentacleType.TENTACLE_DEVICE_POTPOURRY,
            futs=[EnumFut.FUT_UART],
        ),
        Tentacle(
            tag="TENTACLE_DAQ_SALEAE",
            tentacle_type=TentacleType.TENTACLE_DAQ_SALEAE,
            futs=[EnumFut.FUT_I2C],
        ),
    ]
)


@dataclass
class ParameterTentaclesObsolete:
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
    def add_marker(
        cls,
        list_parameters: list[ParameterTentacles],
    ) -> Iterator[pytest.ParameterSet]:
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
        return self._get_tentacle_by_type(TentacleType.TENTACLE_DEVICE_POTPOURRY)

    @property
    def tentacle_daq(self) -> Tentacle:
        return self._get_tentacle_by_type(TentacleType.TENTACLE_DAQ_SALEAE)


def pytest_generate_tests(metafunc: pytest.Metafunc) -> None:
    if "param" in metafunc.fixturenames:
        # Generate test cases based on the user_roles list

        print(metafunc.definition.nodeid)
        for marker in metafunc.definition.own_markers:
            print(f" {marker!r}")

        def get_marker(name: str) -> pytest.Mark:
            for marker in metafunc.definition.own_markers:
                if marker.name == name:
                    return marker
            assert False

        marker_required_tentacles = get_marker(name="required")
        assert isinstance(marker_required_tentacles, pytest.Mark)
        marker_standard = marker_required_tentacles.kwargs["marker"]
        assert isinstance(marker_standard, MarkerStandard)

        if False:
            marker_required_futs = get_marker(name="required_futs")
            futs_types = marker_required_futs.kwargs["fut_types"]
            assert isinstance(futs_types, list)
            required = Required(tentacle_types=marker_standard, fut_types=futs_types)

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

            metafunc.parametrize("param", ParameterTentacles.add_marker(list_test_runs))

        list_list_tentacle = marker_standard.run_factory()
        print(f"required_futs={marker_standard.required_futs}")
        list_test_runs: list[RunStandard] = [
            RunStandard(run_tentacles=l) for l in list_list_tentacle
        ]
        metafunc.parametrize("param", RunStandard.add_marker(list_test_runs))


@pytest.mark.required(
    marker=MarkerStandard(
        required_futs=[EnumFut.FUT_UART],
        required_device_potpourry=True,
        optional_daq_saleae=True,
    )
)
def test_uart(param: RunStandard) -> None:
    if "TENTACLE_MCU_RP2" in param.mcu.tag:
        pytest.skip("mcu not supported")
    print(param.mcu.tag)


@pytest.mark.required(
    marker=MarkerStandard(
        required_futs=[EnumFut.FUT_I2C],
        required_device_potpourry=True,
        optional_daq_saleae=True,
    )
)
def test_i2c(param: RunStandard) -> None:
    if "TENTACLE_MCU_RP2" in param.mcu.tag:
        pytest.skip("mcu not supported")
    print(param.mcu.tag)


class TestPotpourry:
    @pytest.mark.required(
        marker=MarkerStandard(
            required_futs=[EnumFut.FUT_UART],
            required_device_potpourry=True,
        )
    )
    def test_uart(self, param: RunStandard) -> None:
        pass

    @pytest.mark.required(
        marker=MarkerStandard(
            required_futs=[EnumFut.FUT_I2C],
            required_device_potpourry=True,
        )
    )
    def test_i2c(self, param: RunStandard) -> None:
        pass
