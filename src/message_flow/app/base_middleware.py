from contextlib import contextmanager
from typing import Annotated, Generator

from typing_extensions import Doc

from ..utils import external


@external
class BaseMiddleware:
    """
    `BaseMiddleware` class, used to define custom middlewares.

    **Example**

    ```python
    import logging
    from message_flow import BaseMiddleware

    logger = logging.getLogger(__name__)


    class CustomMiddleware(BaseMiddleware):
        def on_consume(self) -> None:
            logger.info("Message with %s payload and %s headers received.", self.payload, self.headers)
            return super().on_consume()

        def after_consume(self, error: Exception | None = None) -> None:
            logger.info("Message with %s payload and %s headers processed.", self.payload, self.headers)
            return super().after_consume(error)

        def on_produce(self) -> None:
            logger.info("Producing message with %s payload and %s headers.", self.payload, self.headers)
            return super().on_produce()

        def after_produce(self, error: Exception | None = None) -> None:
            logger.info("Message with %s payload and %s headers produced.", self.payload, self.headers)
            return super().after_produce(error)
    ```
    """

    def __init__(
        self,
        payload: Annotated[bytes, Doc("Payload of the `Message`.")],
        headers: Annotated[dict[str, str], Doc("Headers of the `Message`.")],
    ) -> None:
        self.payload = payload
        self.headers = headers

    def on_consume(self) -> None:
        """
        Logic to execute before message processing.
        """
        pass

    def after_consume(
        self,
        error: Exception | None = None,
    ) -> None:
        """
        Logic to execute after message processing.
        """
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
        """
        Logic to execute before message producing.
        """
        pass

    def after_produce(
        self,
        error: Exception | None = None,
    ) -> None:
        """
        Logic to execute after message producing.
        """
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
