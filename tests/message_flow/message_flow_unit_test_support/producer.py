from typing import TYPE_CHECKING
from unittest import mock

from message_flow import Channel, Message, MessageFlow

from .fake_message_producer import FakeMessageProducer

if TYPE_CHECKING:
    from .message_flow_unit_test_support import MessageFlowUnitTestSupport


class Producer:
    def __init__(self, parent: "MessageFlowUnitTestSupport") -> None:
        self._parent = parent

        self._app: MessageFlow = MessageFlow(message_producer=FakeMessageProducer(parent))
        self._channel: Channel | None = None
        self._reply_channel: Channel | None = None
        self._reply_handler: mock.Mock | None = None

    def add_channel(self, address: str) -> None:
        try:
            self._channel = Channel(address)
            self._app.add_channel(self._channel)
        except Exception as error:
            self._parent._creation_exception = error

    def add_publication(self, message: type[Message]) -> None:
        try:
            self._channel.publish()(message)
        except Exception as error:
            self._parent._creation_exception = error

    def add_command(self, message: type[Message], reply: type[Message] | None, reply_to: str | None) -> None:
        try:
            if reply is not None and reply_to is not None:
                self._reply_channel = Channel(reply_to)
                self._app.add_channel(self._reply_channel)

                self._reply_handler = mock.MagicMock()
                self._reply_handler.return_value = None

                self._reply_channel.subscribe(reply)(self._reply_handler)

                self._channel.send(reply, self._reply_channel)(message)
            else:
                self._channel.send(reply=reply, reply_channel=reply_to)(message)
        except Exception as error:
            self._parent._creation_exception = error

    def publish(self, message: Message, to: str | None = None) -> None:
        try:
            self._app.publish(message=message, channel_address=to)
        except Exception as error:
            self._parent._error = error

    def send(self, message: Message, address: str | None = None, reply_to: str | None = None) -> None:
        try:
            self._app.send(message=message, channel_address=address, reply_to_address=reply_to)
        except Exception as error:
            self._parent._error = error

    def dispatch(self) -> None:
        try:
            self._app.dispatcher.message_handler(
                self._parent.message_with_channel.payload, self._parent.message_with_channel.headers
            )
        except Exception as error:
            self._parent._error = error

    def is_reply_called(self) -> None:
        self._reply_handler.assert_called_once()
