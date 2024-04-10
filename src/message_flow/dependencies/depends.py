from typing import Any, Callable

from ..utils import external


@external
class Depends:
    def __init__(
        self,
        dependency: Callable[..., Any],
        *,
        use_cache: bool = True,
        cast: bool = True,
    ) -> None:
        self.dependency = dependency
        self.use_cache = use_cache
        self.cast = cast
