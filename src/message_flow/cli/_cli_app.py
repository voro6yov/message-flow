import logging
from collections import defaultdict
from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path
from typing import DefaultDict, final

import typer

from ..app import MessageFlow
from ..utils import internal
from ._documentation_server import DocumentationServer
from ._logging_level import LoggingLevel


@final
@internal
class CLIApp:
    LOGGING_LEVELS: DefaultDict[str, int] = defaultdict(
        lambda: logging.INFO,
        **{
            LoggingLevel.CRITICAL: logging.CRITICAL,
            LoggingLevel.ERROR: logging.ERROR,
            LoggingLevel.WARNING: logging.WARNING,
            LoggingLevel.INFO: logging.INFO,
            LoggingLevel.DEBUG: logging.DEBUG,
        },
    )

    def __init__(self, app_path: str, log_level: LoggingLevel = LoggingLevel.INFO) -> None:
        self.app_path = app_path

        self.instance.set_logging_level(self.LOGGING_LEVELS[log_level])

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
    def instance(self) -> MessageFlow:
        if not hasattr(self, "_instance"):
            try:
                self._instance = self._import()
            except FileNotFoundError as e:
                typer.echo(e, err=True)
                raise typer.BadParameter("Please, input module like [python_module:message_flow_app_name]") from e

        return self._instance

    def dispatch(self) -> None:
        self.instance.dispatch()

    def serve_documentation(self, host: str, port: int) -> None:
        DocumentationServer(studio_page=self.instance.generate_docs_page(), host=host, port=port).serve()

    def _import(self) -> MessageFlow:
        spec = spec_from_file_location(
            "mode",
            f"{self.module_path}.py",
            submodule_search_locations=[str(self.module_path.parent.absolute())],
        )

        if spec is None:
            raise FileNotFoundError(self.module_path)

        module = module_from_spec(spec)
        loader = spec.loader

        if loader is None:
            raise ValueError(f"{spec} has no loader")

        loader.exec_module(module)

        try:
            obj = getattr(module, self.app_name)
        except AttributeError as e:
            raise FileNotFoundError(self.module_path) from e

        return obj
