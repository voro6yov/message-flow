import logging
from typing import final

from ...utils import internal
from .._internal import Channels
from ..messaging import MessageConsumer
from .producer import Producer
from .routing_headers import RoutingHeaders


@final
@internal
class Dispatcher:
    def __init__(self, channels: Channels, message_consumer: MessageConsumer, producer: Producer) -> None:
        self._logger = logging.getLogger(__name__)

        self._channels = channels
        self._message_consumer = message_consumer
        self._producer = producer

    def initialize(self) -> None:
        self._logger.info("Initializing dispatcher")
        self._message_consumer.subscribe(
            self._channels.addresses,
            self.message_handler,
        )
        self._logger.info("Initialized dispatcher")

    def message_handler(self, payload: bytes, headers: dict[str, str]) -> None:
        if (
            handler := self._channels.operation_of(headers[RoutingHeaders.ADDRESS], headers[RoutingHeaders.TYPE])
        ) is None:
            return

        if (message := handler(handler.message.from_payload_and_headers(payload, headers))) is not None:
            self._producer.send(headers[RoutingHeaders.REPLY_TO], message)
