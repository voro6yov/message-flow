from http.server import HTTPServer

from .request_handler import RequestHandler

__all__ = ["serve_schema"]


def serve_schema(
    schema: str,
    host: str,
    port: int,
) -> None:
    RequestHandler.schema = schema

    httpd = HTTPServer((host, port), RequestHandler)

    httpd.serve_forever()
