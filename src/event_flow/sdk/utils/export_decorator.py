import inspect
from typing import TypeVar

__all__ = ["export"]

T = TypeVar("T")


def export(definition: type[T]) -> type[T]:
    def get___all__() -> list[str]:
        for frame, *_ in inspect.getouterframes(inspect.currentframe()):
            if (module := inspect.getmodule(frame)) is not None and module.__name__ == definition.__module__:
                return module.__dict__.setdefault("__all__", [])
        else:
            return list()

    __all__ = get___all__()
    if definition not in __all__:
        __all__.append(definition.__name__)

    return definition
