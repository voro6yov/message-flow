import typer

from ._async_api_schema import serve_schema
from .cli_app import CLIApp
from .logging_level import LoggingLevel

__all__ = ["cli"]

cli = typer.Typer(pretty_exceptions_short=True)


@cli.callback()
def callback():
    """
    Message Flow
    """


@cli.command()
def dispatch(
    app: str = typer.Argument(
        ...,
        help="[python_module:MessageFlow] - path to your application",
    ),
    log_level: LoggingLevel = typer.Option(
        LoggingLevel.INFO,
        case_sensitive=False,
        show_default=False,
        help="[INFO] default",
    ),
):
    """
    Starts message dispatching
    """
    cli_app = CLIApp(app, log_level)

    cli_app.dispatch()


@cli.command()
def docs(
    app: str = typer.Argument(
        ...,
        help="[python_module:MessageFlow] - path to your application",
    ),
    host: str = typer.Option(
        "localhost",
        help="documentation hosting address",
    ),
    port: int = typer.Option(
        8000,
        help="documentation hosting port",
    ),
):
    """
    Starts Async API schema serving
    """
    cli_app = CLIApp(app)

    serve_schema(studio_page=cli_app.generate_docs_page(), host=host, port=port)
