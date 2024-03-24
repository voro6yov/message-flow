from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path
from typing import Any

import typer

from ..utils import internal


@internal
class CLIApp:
    def __init__(self, app_path: str, reload: bool = False) -> None:
        self.app_path = app_path

        self.reload = reload

    @property
    def app_path(self) -> str:
        return self._app_path

    @app_path.setter
    def app_path(self, path: str) -> None:
        if not isinstance(path, str):
            raise typer.BadParameter("Given value is not of type string")

        if ":" not in path:
            raise typer.BadParameter(f"`{path}` is not a MessageFlow")

        self._app_path = path

    @property
    def module_path(self) -> Path:
        if not hasattr(self, "_module_path"):
            module, _ = self.app_path.split(":", 2)

            module_path = Path.cwd()
            for path_element in module.split("."):
                module_path = module_path / path_element

            self._module_path = module_path

        return self._module_path

    @property
    def app_name(self) -> str:
        if not hasattr(self, "_app_name"):
            self._app_name = self.app_path.split(":", 2)[1]

        return self._app_name

    @property
    def instance(self) -> Any:
        try:
            app_object = self._import()
        except FileNotFoundError as e:
            typer.echo(e, err=True)
            raise typer.BadParameter("Please, input module like [python_module:message_flow_app_name]") from e
        else:
            return app_object  # type: ignore

    def dispatch(self) -> None:
        self.instance.dispatch()

    def _import(self) -> Any:
        spec = spec_from_file_location(
            "mode",
            f"{self.module_path}.py",
            submodule_search_locations=[str(self.module_path.parent.absolute())],
        )

        if spec is None:  # pragma: no cover
            raise FileNotFoundError(self.module_path)

        module = module_from_spec(spec)
        loader = spec.loader

        if loader is None:  # pragma: no cover
            raise ValueError(f"{spec} has no loader")

        loader.exec_module(module)

        try:
            obj = getattr(module, self.app_name)
        except AttributeError as e:
            raise FileNotFoundError(self.module_path) from e

        return obj
