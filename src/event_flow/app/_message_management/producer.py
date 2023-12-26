from ...message import Message
from ...utils import internal
from ..messaging import MessageProducer
from .routing_headers import RoutingHeaders


@internal
class Producer:
    def __init__(self, message_producer: MessageProducer) -> None:
        self._message_producer = message_producer

    def send(self, channel: str, message: Message) -> None:
        message.add_headers(self._make_routing_info(channel, message.message_id))

        self._message_producer.send(channel, message.payload, message.headers)

    def _make_routing_info(self, channel: str, type: str) -> dict[str, str]:
        return {
            RoutingHeaders.TYPE: type,
            RoutingHeaders.ADDRESS: channel,
        }
