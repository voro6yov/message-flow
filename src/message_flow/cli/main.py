import typer

from .cli_app import CLIApp

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
    reload: bool = typer.Option(
        False,
        "--reload",
        is_flag=True,
        help="Restart app at directory files changes",
    ),
):
    """
    Shoot the portal gun
    """
    cli_app = CLIApp(app, reload)

    cli_app.dispatch()
