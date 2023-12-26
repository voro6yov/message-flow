import json
import logging
from typing import final

from ..channel import Channel
from ..message import Message
from ..shared import Components
from ..utils import external
from ._internal import EventFlowSchema, Info
from ._message_management import Dispatcher, Producer
from .messaging import MessageConsumer, MessageProducer


@final
@external
class EventFlow:
    def __init__(
        self,
        *,
        channels: list[Channel] | None = None,
        message_producer: MessageProducer,
        message_consumer: MessageConsumer,
        title: str = "EventFlow",
        version: str = "0.1.0",
    ) -> None:
        self._logger = logging.getLogger(self.__class__.__name__)

        self.async_api_version: str = "3.0.0"
        self.title = title
        self.version = version

        self._channels = channels if channels is not None else []
        self._message_producer = message_producer
        self._message_consumer = message_consumer

    @property
    def producer(self) -> Producer:
        if not hasattr(self, "_producer"):
            self._producer = Producer(self._message_producer)
        return self._producer

    @property
    def dispatcher(self) -> Dispatcher:
        if not hasattr(self, "_dispatcher"):
            self._dispatcher = Dispatcher(self._channels, self._message_consumer)
        return self._dispatcher

    def publish(self, message: Message) -> None:
        if (channel := next(filter(lambda c: c.sends(message), self._channels), None)) is None:
            raise RuntimeError(f"Could not find channel for {message}")

        self.producer.send(channel.address, message)

    def dispatch(self) -> None:
        try:
            self.dispatcher.initialize()
            self._message_consumer.start_consuming()
        except Exception as error:
            self._logger.error("An error occurred while dispatching events", exc_info=error)
        finally:
            self._message_consumer.close()
            self._message_producer.close()

    def make_async_api_schema(self) -> str:
        channels_schema = {}
        operations_schema = {}
        components = Components()

        for channel in self._channels:
            channels_schema.update(channel.__async_api_reference__.as_component())
            for operation in channel.operations:
                operations_schema.update(operation.__async_api_reference__.as_component())

            components.merge(channel.__async_api_components__)

        schema = EventFlowSchema(
            asyncapi=self.async_api_version,
            info=Info(title=self.title, version=self.version),
            channels=channels_schema,
            operations=operations_schema,
            components=components.as_schema(),
        )

        return json.dumps(schema)
