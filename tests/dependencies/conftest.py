import pytest

from message_flow.dependencies import Depends


@pytest.fixture
def simple_func():
    def dep_func(a: int) -> int:
        return a

    def func(a: int, b: int = Depends(dep_func)) -> int:
        return a + int(b)

    return func
