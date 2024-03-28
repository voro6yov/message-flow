from http.server import BaseHTTPRequestHandler

from ...utils import internal


@internal
class RequestHandler(BaseHTTPRequestHandler):
    studio_page: str

    def do_GET(self):
        if self.path == "/async-api-docs":
            self._send_async_api_studio_page()
        else:
            self._send_not_found()

    def _send_async_api_studio_page(self) -> None:
        self._set_headers()
        self.wfile.write(self.studio_page.encode())

    def _send_not_found(self) -> None:
        self._set_headers(404, "text/plain")
        self.wfile.write(b"404 Not Found")

    def _set_headers(self, status: int = 200, content_type: str = "text/html"):
        self.send_response(status)
        self.send_header("Content-type", content_type)
        self.end_headers()
