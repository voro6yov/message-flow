import typer

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
    Shoot the portal gun
    """
    cli_app = CLIApp(app, log_level)

    cli_app.dispatch()
