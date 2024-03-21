import importlib
import inspect
import pkgutil
import types
from typing import Generator, TypeVar

__all__ = ["external", "internal", "get_package_modules", "init_package"]

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


def get_current_package(package_name: str) -> types.ModuleType:
    for frame, *_ in inspect.getouterframes(inspect.currentframe()):
        if (module := inspect.getmodule(frame)) is not None and module.__name__ == package_name:
            return module

    raise RuntimeError("Cannot find current package.")


def get_package_modules(package: types.ModuleType) -> Generator[types.ModuleType, None, None]:
    return (
        importlib.import_module(f"{package.__package__}.{module_name}")
        for _, module_name, _ in pkgutil.walk_packages(package.__path__)
        if not module_name.startswith("_")
    )


def init_package(package_name: str) -> None:
    def make_stub_path() -> str:
        return f"{package.__path__[0]}/__init__.pyi"

    def make_import_line() -> str:
        return f"from .{package_module.__name__.split('.')[-1]} import *\n"

    package = get_current_package(package_name)
    package.__dict__.setdefault("__all__", [])

    with open(make_stub_path(), "a+") as stub_file:
        stub_file.truncate(0)
        for package_module in get_package_modules(package):
            stub_file.write(make_import_line())
            package.__dict__.update({name: getattr(package_module, name) for name in package_module.__all__})
            package.__dict__["__all__"] += package_module.__all__
