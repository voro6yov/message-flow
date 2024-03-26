import json
from http.server import BaseHTTPRequestHandler

from ...utils import internal


@internal
class RequestHandler(BaseHTTPRequestHandler):
    schema: str

    def do_GET(self):
        if self.path == "/async-api-docs":
            self._send_async_api_schema()
        else:
            self._send_not_found()

    def _send_async_api_schema(self) -> None:
        self._set_headers()
        self.wfile.write(self._make_asyncapi_html().encode())

    def _send_not_found(self) -> None:
        self._set_headers(404, "text/plain")
        self.wfile.write(b"404 Not Found")

    def _set_headers(self, status: int = 200, content_type: str = "text/html"):
        self.send_response(status)
        self.send_header("Content-type", content_type)
        self.end_headers()

    def _make_asyncapi_html(
        self,
    ) -> str:
        config = {
            "schema": self.schema,
            "config": {
                "show": {
                    "sidebar": True,
                    "info": True,
                    "servers": True,
                    "operations": True,
                    "messages": True,
                    "schemas": True,
                    "errors": True,
                },
                "expand": {
                    "messageExamples": True,
                },
                "sidebar": {
                    "showServers": "byDefault",
                    "showOperations": "byDefault",
                },
            },
        }

        return (
            """
        <!DOCTYPE html>
        <html>
            <head>
        """
            f"""
            <title>MessageFlow AsyncAPI</title>
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
                AsyncApiStandalone.render({json.dumps(config)}, document.getElementById('asyncapi'));
        """
            """
            </script>
            </body>
        </html>
        """
        )
