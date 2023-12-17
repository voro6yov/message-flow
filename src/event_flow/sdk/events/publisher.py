from ..application import Message
from ..messaging import MessageProducer
from ..utils import export
from .routing_headers import RoutingHeaders


@export
class EventPublisher:
    def __init__(self, message_producer: MessageProducer) -> None:
        self._message_producer = message_producer

    def publish(self, channel: str, event: Message) -> None:
        event.add_headers(self._make_routing_info(channel, event.type))

        self._message_producer.send(channel, event.payload, event.headers)

    def _make_routing_info(self, channel: str, type: str) -> dict[str, str]:
        return {
            RoutingHeaders.TYPE: type,
            RoutingHeaders.ADDRESS: channel,
        }
