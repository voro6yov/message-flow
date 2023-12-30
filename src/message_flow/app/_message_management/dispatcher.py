import logging
from typing import final

from ...channel import Channel
from ...operation import Operation
from ...utils import internal
from ..messaging import MessageConsumer
from .producer import Producer
from .routing_headers import RoutingHeaders


@final
@internal
class Dispatcher:
    def __init__(self, channels: list[Channel], message_consumer: MessageConsumer, producer: Producer) -> None:
        self._logger = logging.getLogger(self.__class__.__name__)

        self._channels = channels
        self._message_consumer = message_consumer
        self._producer = producer

    @property
    def addresses(self) -> set[str]:
        if not hasattr(self, "_addresses"):
            self._addresses = {channel.address for channel in self._channels}
        return self._addresses

    def initialize(self) -> None:
        self._logger.info("Initializing dispatcher")
        self._message_consumer.subscribe(
            self.addresses,
            self.message_handler,
        )
        self._logger.info("Initialized dispatcher")

    def message_handler(self, payload: bytes, headers: dict[str, str]) -> None:
        if (handler := self._find_target_operation(headers)) is None:
            return

        if (message := handler(handler.message.from_payload_and_headers(payload, headers))) is not None:
            self._producer.send(headers[RoutingHeaders.REPLY_TO], message)

    def _find_target_operation(self, headers: dict[str, str]) -> Operation | None:
        for channel in self._channels:
            if (
                operation := channel.receives(
                    headers[RoutingHeaders.ADDRESS],
                    headers[RoutingHeaders.TYPE],
                )
            ) is not None:
                return operation
