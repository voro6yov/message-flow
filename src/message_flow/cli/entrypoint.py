import typer

from ._cli_app import CLIApp
from ._logging_level import LoggingLevel

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
    CLIApp(app).serve_documentation(host, port)
