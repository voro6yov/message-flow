import inspect
from typing import TypeVar

__all__ = ["external", "internal"]

T = TypeVar("T")


def get___all__(definition: type[T]) -> list[str]:
    for frame, *_ in inspect.getouterframes(inspect.currentframe()):
        if (module := inspect.getmodule(frame)) is not None and module.__name__ == definition.__module__:
            return module.__dict__.setdefault("__all__", [])
    else:
        return list()


def external(definition: type[T]) -> type[T]:
    __all__ = get___all__(definition)
    if definition not in __all__:
        __all__.append(definition.__name__)

    return definition


def internal(definition: type[T]) -> type[T]:
    __all__ = get___all__(definition)
    if definition not in __all__:
        __all__.append(definition.__name__)

    return definition
