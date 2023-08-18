import abc
from typing import Protocol

from event_flow.utils import export

from .message_handler import MessageHandler
from .message_subscription import MessageSubscription


@export
class MessageConsumer(Protocol):
    @abc.abstractmethod
    def subscribe(
        self,
        subscriber_id: str,
        channels: set[str],
        handler: MessageHandler,
        *,
        queue: str | None = None,
    ) -> MessageSubscription:
        pass

    @property
    @abc.abstractmethod
    def id(self) -> str:
        pass

    @abc.abstractmethod
    def close(self) -> None:
        pass
