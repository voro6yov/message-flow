from http.server import HTTPServer

from .request_handler import RequestHandler

__all__ = ["serve_schema"]


def serve_schema(
    studio_page: str,
    host: str,
    port: int,
) -> None:
    RequestHandler.studio_page = studio_page

    httpd = HTTPServer((host, port), RequestHandler)

    httpd.serve_forever()
