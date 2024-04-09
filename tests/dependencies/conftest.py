import pytest


@pytest.fixture
def simple_func():
    def func(a: int, b: str) -> int:
        return a + int(b)

    return func
