from event_flow.utils import export

from .message import Message
from .message_impl import MessageImpl


@export
class MessageBuilder:
    def __init__(self, body: str, *, headers: dict[str, str] | None = None) -> None:
        self._body = body
        self._headers = headers if headers is not None else {}

    @classmethod
    def with_message(cls, message: Message) -> "MessageBuilder":
        return cls(message.payload, headers=message.headers)

    @classmethod
    def with_payload(cls, payload: str) -> "MessageBuilder":
        return cls(payload)

    def with_header(self, name: str, value: str) -> "MessageBuilder":
        self._headers[name] = value
        return self

    def with_extra_headers(self, prefix: str, headers: dict[str, str]) -> "MessageBuilder":
        for key, value in headers.items():
            self._headers[prefix + key] = value

        return self

    def build(self) -> Message:
        return MessageImpl(self._body, self._headers)
