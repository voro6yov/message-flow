import logging
from contextlib import ExitStack
from typing import final

from ...utils import internal
from .._internal import Channels
from ..base_middleware import BaseMiddleware
from ..messaging import MessageConsumer
from .producer import Producer
from .routing_headers import RoutingHeaders


@final
@internal
class Dispatcher:
    def __init__(
        self,
        channels: Channels,
        message_consumer: MessageConsumer,
        producer: Producer,
        logger: logging.Logger,
    ) -> None:
        self._logger = logger

        self._channels = channels
        self._message_consumer = message_consumer
        self._producer = producer
        self._middlewares: list[type[BaseMiddleware]] = []

    def initialize(self) -> None:
        self._logger.debug("Initializing dispatcher")
        self._message_consumer.subscribe(
            self._channels.addresses,
            self.message_handler,
        )
        self._logger.debug("Initialized dispatcher")

    def add_middleware(self, middleware: type[BaseMiddleware]) -> None:
        self._middlewares.append(middleware)

    def message_handler(self, payload: bytes, headers: dict[str, str]) -> None:
        if (
            handler := self._channels.operation_of(headers[RoutingHeaders.ADDRESS], headers[RoutingHeaders.TYPE])
        ) is None:
            return

        with ExitStack() as dispatcher_stack:
            self._execute_consume_middlewares(dispatcher_stack, payload, headers)

            if (message := handler(handler.message.from_payload_and_headers(payload, headers))) is not None:
                self._execute_produce_middlewares(dispatcher_stack, message.payload, message.headers)

                self._producer.send(headers[RoutingHeaders.REPLY_TO], message)

    def _execute_consume_middlewares(self, stack: ExitStack, payload: bytes, headers: dict[str, str]) -> None:
        for middleware in self._middlewares:
            stack.enter_context(middleware(payload, headers).consume())

    def _execute_produce_middlewares(self, stack: ExitStack, payload: bytes, headers: dict[str, str]) -> None:
        for middleware in self._middlewares:
            stack.enter_context(middleware(payload, headers).produce())
