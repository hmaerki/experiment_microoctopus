import pytest

from test_fut_uart import INFRASTRUCTURE, Combinations, EnumFut, TentacleType


class TentacleMcu:
    pass


class TentacleDevicePotpourry:
    pass


class TentacleDaqSaleae:
    pass


def pytest_generate_tests(metafunc: pytest.Metafunc) -> None:
    required_tentacle_types = []
    if "mcu" in metafunc.fixturenames:
        required_tentacle_types.append(TentacleType.TENTACLE_MCU)
        # metafunc.parametrize("mcu", 'param_mcu')

    if "device_potpourry" in metafunc.fixturenames:
        required_tentacle_types.append(TentacleType.TENTACLE_DEVICE_POTPOURRY)
        # metafunc.parametrize("device_potpourry", 'param_potpourry')

    if "daq_saleae" in metafunc.fixturenames:
        required_tentacle_types.append(TentacleType.TENTACLE_DEVICE_POTPOURRY)
        # metafunc.parametrize("daq_saleae", 'param_daq')

    # if "param" in metafunc.fixturenames:
    if True:
        # Generate test cases based on the user_roles list

        print(metafunc.definition.nodeid)
        for marker in metafunc.definition.own_markers:
            print(f" {marker!r}")

        def get_marker(name: str) -> pytest.Mark:
            for marker in metafunc.definition.own_markers:
                if marker.name == name:
                    return marker
            assert False

        marker_required_futs = get_marker(name="required_futs")
        futs_types = marker_required_futs.kwargs["fut_types"]
        assert isinstance(futs_types, list)
        if False:
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

        print(f"required_futs={futs_types}")
        c = Combinations(
            tentacles=INFRASTRUCTURE.tentacles,
            required_futs=futs_types,
            tentacle_types=required_tentacle_types,
            optional_tentacle_types=[],
        )
        list_list_tentacle = list(c.combination_with_optional_tentacles())

        if "mcu" in metafunc.fixturenames:
            required_tentacle_types.append(TentacleType.TENTACLE_MCU)
            metafunc.parametrize("mcu", "param_mcu")

        if "device_potpourry" in metafunc.fixturenames:
            required_tentacle_types.append(TentacleType.TENTACLE_DEVICE_POTPOURRY)
            # metafunc.parametrize("device_potpourry", 'param_potpourry')

        if "daq_saleae" in metafunc.fixturenames:
            required_tentacle_types.append(TentacleType.TENTACLE_DEVICE_POTPOURRY)

        list_test_runs: list[RunStandard] = [
            RunStandard(run_tentacles=l) for l in list_list_tentacle
        ]
        metafunc.parametrize("param", RunStandard.add_marker(list_test_runs))


@pytest.mark.required_futs(fut_types=[EnumFut.FUT_UART])
def test_uart(
    mcu: TentacleMcu,
    device_potpourry: TentacleDevicePotpourry,
) -> None:
    if "TENTACLE_MCU_RP2" in mcu.tag:
        pytest.skip("mcu not supported")
    print(mcu.tag)


@pytest.mark.required_futs(fut_types=[EnumFut.FUT_I2C])
def test_i2c(
    mcu: TentacleMcu,
    device_potpourry: TentacleDevicePotpourry,
    daq_saleae: TentacleDaqSaleae,
) -> None:
    if "TENTACLE_MCU_RP2" in mcu.tag:
        pytest.skip("mcu not supported")
    print(mcu.tag)


class TestPotpourry:
    @pytest.mark.required_futs(fut_types=[EnumFut.FUT_UART])
    def test_uart(
        self,
        mcu: TentacleMcu,
        device_potpourry: TentacleDevicePotpourry,
    ) -> None:
        pass

    @pytest.mark.required_futs(fut_types=[EnumFut.FUT_I2C])
    def test_i2c(
        self,
        mcu: TentacleMcu,
        device_potpourry: TentacleDevicePotpourry,
    ) -> None:
        pass
