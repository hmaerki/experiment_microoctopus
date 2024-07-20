import pytest

from tests.test_fut_uart import EnumFut

if False:
    @pytest.fixture(scope="function", params=[1, 2], indirect=True)
    def otherarg(request):
        param = request.param
        print("  SETUP otherarg", param)
        yield param
        print("  TEARDOWN otherarg", param)

if False:
    @pytest.fixture()
    def mcu(request):
        param = request.param
        print("  SETUP param", param)
        yield param
        print("  TEARDOWN param", param)

def pytest_generate_tests(metafunc: pytest.Metafunc) -> None:
    # marker = request.node.get_closest_marker("required_futs")
    # assert marker is not None

    if True:
        print(metafunc.definition.nodeid)
        for marker in metafunc.definition.own_markers:
            print(f" {marker!r}")

        def get_marker(name: str) -> pytest.Mark:
            for marker in metafunc.definition.own_markers:
                if marker.name == name:
                    return marker
            assert False

        marker_required_futs = get_marker(name="required_futs")
        assert isinstance(marker_required_futs, pytest.Mark)
        fut_types = marker_required_futs.kwargs["fut_types"]
        assert isinstance(fut_types, list)

    if "mcu" in metafunc.fixturenames:
            metafunc.parametrize("mcu", ['RP2', 'PYBORAD'])
    if "device_potpourry" in metafunc.fixturenames:
            metafunc.parametrize("device_potpourry", ['a', 'b'])
            
@pytest.mark.required_futs(fut_types=[EnumFut.FUT_I2C])
def test_0(mcu, device_potpourry):
    print("  RUN test0 with otherarg", mcu, device_potpourry)
