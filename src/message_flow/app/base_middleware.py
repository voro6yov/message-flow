from contextlib import contextmanager
from typing import Generator

from ..utils import external


@external
class BaseMiddleware:
    def __init__(self, payload: bytes, headers: dict[str, str]) -> None:
        self.payload = payload
        self.headers = headers

    def on_consume(self) -> None:
        pass

    def after_consume(
        self,
        error: Exception | None = None,
    ) -> None:
        if error is not None:
            raise error

    @contextmanager
    def consume(self) -> Generator[None, None, None]:
        consume_error: Exception | None = None

        try:
            self.on_consume()
            yield
        except Exception as error:
            consume_error = error

        self.after_consume(consume_error)

    def on_produce(self) -> None:
        pass

    def after_produce(
        self,
        error: Exception | None = None,
    ) -> None:
        if error is not None:
            raise error

    @contextmanager
    def produce(self) -> Generator[None, None, None]:
        produce_error: Exception | None = None

        try:
            self.on_produce()
            yield
        except Exception as error:
            produce_error = error

        self.after_produce(produce_error)
