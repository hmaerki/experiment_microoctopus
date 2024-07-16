"""
`tests/08_params_test.py` shows how to write parametrized tests.


This examples demonstrates how to write parametrized tests using dataclasses.
Benefits are:
* Type safety.
* Ease to add/remove parameters.
* Ease to control the id (in pytest displayed within [])
* May be used in standalone tests without pytest.
"""
from dataclasses import dataclass
import pytest


@dataclass
class ParameterX:
    """
    Our test parameters are just objects of this class.
    With this class we may control it's name.
    The use of the class is typesafe - the pytest-approach is not typesafe!
    """

    a: int
    b: int
    expected_result: int
    identifier_note: str = None
    smoke: bool = False

    def __post_init__(self):
        """
        You may check for correct datatypes here.
        Or use pydantic which does this for you.
        """
        assert isinstance(self.a, int)
        assert isinstance(self.b, int)
        assert isinstance(self.expected_result, int)
        assert isinstance(self.identifier_note, (type(None), str))
        assert isinstance(self.smoke, bool)

    @property
    def identifier(self) -> str:
        """
        This will be the paramter [...] used by pytest.
        """
        ident = f"{self.a}-{self.b}"
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


parameters = ParameterX.add_marker(
    [
        ParameterX(
            a=3,
            b=3,
            expected_result=9,
        ),
        ParameterX(
            a=1,
            b=32,
            expected_result=32,
            identifier_note="-very-special-testcase",
            smoke=True,
        ),
        ParameterX(
            a=2,
            b=2,
            expected_result=4,
        ),
    ]
)


@pytest.mark.parametrize("param", parameters)
def test_x(param: ParameterX):
    assert param.a * param.b == param.expected_result
