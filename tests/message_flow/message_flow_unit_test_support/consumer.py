from typing import TYPE_CHECKING
from unittest import mock

from message_flow import Message, MessageFlow

from .fake_message_producer import FakeMessageProducer

if TYPE_CHECKING:
    from .message_flow_unit_test_support import MessageFlowUnitTestSupport


class Consumer:
    def __init__(self, parent: "MessageFlowUnitTestSupport") -> None:
        self._parent = parent

        self._app: MessageFlow = MessageFlow(message_producer=FakeMessageProducer(parent))
        self._address: str | None = None
        self._handler: mock.Mock | None = None

    def add_address(self, address: str) -> None:
        self._address = address

    def add_publication(self, message: type[Message]) -> None:
        self._handler = mock.MagicMock()
        self._handler.return_value = None

        self._app.subscribe(address=self._address, message=message)(self._handler)

    def add_command(self, message: type[Message], reply: Message | None) -> None:
        self._handler = mock.MagicMock()
        self._handler.return_value = reply

        self._app.subscribe(address=self._address, message=message)(self._handler)

    def dispatch(self) -> None:
        try:
            self._app.dispatcher.message_handler(
                self._parent.message_with_channel.payload, self._parent.message_with_channel.headers
            )
        except Exception as error:
            self._parent._error = error

    def is_handler_called(self) -> None:
        self._handler.assert_called_once()

    def is_handler_not_called(self) -> None:
        self._handler.assert_not_called()
