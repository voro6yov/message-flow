import logging

from ..events import EventDispatcher, EventPublisher
from ..messaging import MessageConsumer, MessageProducer
from ..utils import export
from .channel import Channel
from .message import Message


@export
class EventFlow:
    def __init__(
        self,
        *,
        channels: list[Channel],
        message_producer: MessageProducer,
        message_consumer: MessageConsumer,
    ) -> None:
        self._logger = logging.getLogger(self.__class__.__name__)

        self._channels = channels
        self._message_producer = message_producer
        self._message_consumer = message_consumer

    @property
    def event_publisher(self) -> EventPublisher:
        if not hasattr(self, "_event_publisher"):
            self._event_publisher = EventPublisher(self._message_producer)
        return self._event_publisher

    @property
    def event_dispatcher(self) -> EventDispatcher:
        if not hasattr(self, "_event_dispatcher"):
            self._event_dispatcher = EventDispatcher(self._channels, self._message_consumer)
        return self._event_dispatcher

    def publish(self, event: Message) -> None:
        if (channel := next(filter(lambda c: c.sends(event), self._channels), None)) is None:
            raise RuntimeError(f"Could not find channel for {event}")

        self.event_publisher.publish(channel.address, event)

    def dispatch(self) -> None:
        try:
            self.event_dispatcher.initialize()
            self._message_consumer.start_consuming()
        except Exception as error:
            self._logger.error("An error occurred while dispatching events", exc_info=error)
        finally:
            self._message_consumer.close()
            self._message_producer.close()
