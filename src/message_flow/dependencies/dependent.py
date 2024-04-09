from typing import Callable

from ..utils import internal


@internal
class Dependent:
    def __init__(self, call: Callable) -> None:
        self._call = call

    @classmethod
    def for_call(cls, *, call: Callable) -> "Dependent":
        return Dependent(call=call)
