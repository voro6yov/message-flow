from typing import TYPE_CHECKING

from message_flow import MessageProducer

from .message_with_channel import MessageWithChannel

if TYPE_CHECKING:
    from .message_flow_unit_test_support import MessageFlowUnitTestSupport


class FakeMessageProducer(MessageProducer):
    def __init__(self, parent: "MessageFlowUnitTestSupport") -> None:
        self.parent = parent

    def send(self, channel: str, payload: bytes, headers: dict[str, str] | None = None) -> None:
        self.parent.message_with_channel = MessageWithChannel(channel, payload, headers)

    def close(self) -> None:
        ...
