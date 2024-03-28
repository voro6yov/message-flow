import json

from ....utils import internal
from .config import AsyncAPIStudio, AsyncAPIStudioConfig, ExpandingOptions, ShowingOptions, SidebarOptions


@internal
class AsyncAPIStudioPage:
    def __init__(
        self,
        schema: str,
        title: str,
        sidebar: bool,
        info: bool,
        servers: bool,
        operations: bool,
        messages: bool,
        schemas: bool,
        errors: bool,
    ) -> None:
        self._studio = AsyncAPIStudio(
            schema=schema,
            config=AsyncAPIStudioConfig(
                show=ShowingOptions(
                    sidebar=sidebar,
                    info=info,
                    servers=servers,
                    operations=operations,
                    messages=messages,
                    schemas=schemas,
                    errors=errors,
                ),
                expand=ExpandingOptions(messageExamples=True),
                sidebar=SidebarOptions(
                    showOperations="byDefault",
                    showServers="byDefault",
                ),
            ),
        )

        self._title = title

    def generate(self) -> str:
        return (
            """
        <!DOCTYPE html>
        <html>
            <head>
        """
            f"""
            <title>{self._title} AsyncAPI</title>
        """
            """
            <link rel="icon" href="https://www.asyncapi.com/favicon.ico">
            <link rel="icon" type="image/png" sizes="16x16" href="https://www.asyncapi.com/favicon-16x16.png">
            <link rel="icon" type="image/png" sizes="32x32" href="https://www.asyncapi.com/favicon-32x32.png">
            <link rel="icon" type="image/png" sizes="194x194" href="https://www.asyncapi.com/favicon-194x194.png">
            <link rel="stylesheet" href="https://unpkg.com/@asyncapi/react-component@1.4.2/styles/default.min.css">
            </head>

            <style>
            html {
                font-family: ui-sans-serif,system-ui,-apple-system,BlinkMacSystemFont,Segoe UI,Roboto,Helvetica Neue,Arial,Noto Sans,sans-serif,Apple Color Emoji,Segoe UI Emoji,Segoe UI Symbol,Noto Color Emoji;
                line-height: 1.5;
            }
            </style>

            <body>
            <div id="asyncapi"></div>

            <script src="https://unpkg.com/@asyncapi/react-component@1.4.2/browser/standalone/index.js"></script>
            <script>
        """
            f"""
                AsyncApiStandalone.render({json.dumps(self._studio)}, document.getElementById('asyncapi'));
        """
            """
            </script>
            </body>
        </html>
        """
        )
