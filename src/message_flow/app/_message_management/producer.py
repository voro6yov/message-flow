from typing import final

from ...message import Message
from ...utils import internal
from ..messaging import MessageProducer
from .routing_headers import RoutingHeaders


@final
@internal
class Producer:
    def __init__(self, message_producer: MessageProducer) -> None:
        self._message_producer = message_producer

    def send(self, channel: str, message: Message, reply_to_address: str | None = None) -> None:
        message.add_routing_headers(self._make_routing_info(channel, message.message_id, reply_to_address))

        self._message_producer.send(channel, message.payload, message.headers)

    def _make_routing_info(self, channel: str, type: str, reply_to_address: str | None) -> dict[str, str]:
        routing_info = {
            RoutingHeaders.TYPE: type,
            RoutingHeaders.ADDRESS: channel,
        }

        if reply_to_address is not None:
            routing_info[RoutingHeaders.REPLY_TO] = reply_to_address

        return routing_info
