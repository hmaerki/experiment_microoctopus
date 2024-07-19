from pytest import fixture

from test_utils import break_into_debugger_on_exception

# Uncomment to following line
# to stop tests on exceptions
break_into_debugger_on_exception(globals())


@fixture
def global_fixture():
    print("\n(Doing global fixture setup stuff!)")
