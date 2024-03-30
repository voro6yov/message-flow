from typing import Callable, Protocol

from ..utils import internal


@internal
class FastAPI(Protocol):
    def add_route(
        self,
        path: str,
        route: Callable,
        include_in_schema: bool = True,
    ) -> None: ...
