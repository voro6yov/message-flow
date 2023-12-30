import json
import logging
from typing import Callable, final

from ..channel import Channel
from ..message import Message
from ..operation import Operation
from ..shared import Components
from ..utils import external
from ._internal import Info, MessageFlowSchema
from ._message_management import Dispatcher, Producer
from ._simple_messaging import SimpleMessageConsumer, SimpleMessageProducer
from .messaging import MessageConsumer, MessageProducer

MessageHandler = Callable[[Message], Message | None]


@final
@external
class MessageFlow:
    def __init__(
        self,
        *,
        channels: list[Channel] | None = None,
        message_producer: MessageProducer | None = None,
        message_consumer: MessageConsumer | None = None,
        title: str = "MessageFlow",
        version: str = "0.1.0",
    ) -> None:
        self._logger = logging.getLogger(self.__class__.__name__)

        self.async_api_version: str = "3.0.0"
        self.title = title
        self.version = version

        self._channels = channels or []
        self._message_producer = message_producer or SimpleMessageProducer()
        self._message_consumer = message_consumer or SimpleMessageConsumer()

    @property
    def producer(self) -> Producer:
        if not hasattr(self, "_producer"):
            self._producer = Producer(self._message_producer)
        return self._producer

    @property
    def dispatcher(self) -> Dispatcher:
        if not hasattr(self, "_dispatcher"):
            self._dispatcher = Dispatcher(self._channels, self._message_consumer, self.producer)
        return self._dispatcher

    def subscribe(self, address: str, message: type[Message]) -> Callable[[MessageHandler], MessageHandler]:
        channel = self._find_or_create_channel(address)
        return channel.subscribe(message)

    def publish(self, message: Message, *, channel_address: str | None = None) -> None:
        if (channel := self._find_channel(message)) is None and channel_address is None:
            raise RuntimeError(f"Could not find channel for {message}")

        self.producer.send(
            channel=channel.address if channel is not None else channel_address,  # type: ignore
            message=message,
        )

    def send(
        self, message: Message, *, channel_address: str | None = None, reply_to_address: str | None = None
    ) -> None:
        channel, operation = self._find_channel_and_operation(message) or (None, None)

        if channel is None and channel_address is None:
            raise RuntimeError(f"Could not find channel for {message}")

        self.producer.send(
            channel=channel.address if channel is not None else channel_address,  # type: ignore
            message=message,
            reply_to_address=operation.reply.channel if operation is not None else reply_to_address,
        )

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

        schema = MessageFlowSchema(
            asyncapi=self.async_api_version,
            info=Info(title=self.title, version=self.version),
            channels=channels_schema,
            operations=operations_schema,
            components=components.as_schema(),
        )

        return json.dumps(schema)

    def _find_channel(self, message: Message) -> Channel | None:
        return next(filter(lambda c: c.sends(message.message_id), self._channels), None)

    def _find_channel_and_operation(self, message: Message) -> tuple[Channel, Operation] | None:
        for channel in self._channels:
            for operation in channel.operations:
                if operation.sends(message.message_id):
                    return channel, operation

    def _find_or_create_channel(self, address: str) -> Channel:
        if (channel := next(filter(lambda c: c.address == address, self._channels), None)) is None:
            channel = Channel(address)
            self._channels.append(channel)

        return channel
