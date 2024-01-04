from message_flow import Message

from .consumer import Consumer
from .message_with_channel import MessageWithChannel
from .producer import Producer


class MessageFlowUnitTestSupport:
    def __init__(self) -> None:
        self.message_with_channel: MessageWithChannel = None

        self._producer: Producer | None = None
        self._consumer: Consumer | None = None

        self._creation_exception: Exception | None = None
        self._error: Exception | None = None

    @classmethod
    def given(cls) -> "MessageFlowUnitTestSupport":
        return cls()

    def publisher(self) -> "MessageFlowUnitTestSupport":
        self._producer = Producer(self)
        return self

    def sender(self) -> "MessageFlowUnitTestSupport":
        self._producer = Producer(self)
        return self

    def with_channel(self, address: str) -> "MessageFlowUnitTestSupport":
        self._producer.add_channel(address)

        return self

    def for_event(self, message: type[Message]) -> "MessageFlowUnitTestSupport":
        self._producer.add_publication(message)

        return self

    def for_command(
        self,
        message: type[Message],
        reply: type[Message] | None = None,
        reply_to: str | None = None,
    ) -> "MessageFlowUnitTestSupport":
        self._producer.add_command(message, reply, reply_to)

        return self

    def and_with_channel(self, address: str) -> "MessageFlowUnitTestSupport":
        self._producer.add_channel(address)

        return self

    def dispatcher(self) -> "MessageFlowUnitTestSupport":
        self._consumer = Consumer(self)
        return self

    def subscribed_to(self, address: str) -> "MessageFlowUnitTestSupport":
        self._consumer.add_address(address)

        return self

    def with_event(self, message: type[Message]) -> "MessageFlowUnitTestSupport":
        self._consumer.add_publication(message)

        return self

    def with_command(self, message: type[Message], reply: Message | None = None) -> "MessageFlowUnitTestSupport":
        self._consumer.add_command(message, reply)

        return self

    def and_subscribe_to(self, address: str) -> "MessageFlowUnitTestSupport":
        self._consumer.add_address(address)

        return self

    def expect(self) -> "MessageFlowUnitTestSupport":
        if self._creation_exception is not None:
            raise RuntimeError(f"Message Flow creation failed with error. ({self._creation_exception})")

        return self

    def publish(self, message: Message, to: str | None = None) -> "MessageFlowUnitTestSupport":
        self._producer.publish(message, to)

        return self

    def send(
        self, message: Message, address: str | None = None, reply_to: str | None = None
    ) -> "MessageFlowUnitTestSupport":
        self._producer.send(message=message, address=address, reply_to=reply_to)

        return self

    def dispatch(self) -> "MessageFlowUnitTestSupport":
        self._consumer.dispatch()

        return self

    def dispatch_reply(self) -> "MessageFlowUnitTestSupport":
        self._producer.dispatch()

        return self

    def and_given(self) -> "MessageFlowUnitTestSupport":
        return self

    def expect_successful_send(self, message: Message, to: str) -> "MessageFlowUnitTestSupport":
        if self.message_with_channel.checked:
            raise RuntimeError("Message already was checked.")

        assert to == self.message_with_channel.channel
        assert message.__class__.__name__ == self.message_with_channel.message_type

        self.message_with_channel.mark_checked()

        return self

    def expect_successful_consume(self) -> "MessageFlowUnitTestSupport":
        self._consumer.is_handler_called()

        return self

    def expect_successful_reply_consume(self) -> "MessageFlowUnitTestSupport":
        self._producer.is_reply_called()

        return self

    def expect_no_consume(self) -> "MessageFlowUnitTestSupport":
        self._consumer.is_handler_not_called()

        return self

    def expect_error(self, error: type[Exception] | None = None) -> "MessageFlowUnitTestSupport":
        assert self._error is not None
        if self._error is not None and error is not None:
            assert type(self._error) == error

        return self

    def expect_no_messages_was_sent(self) -> "MessageFlowUnitTestSupport":
        assert self.message_with_channel.checked
