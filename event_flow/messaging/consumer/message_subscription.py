import abc
from typing import Protocol

from event_flow.utils import export


@export
class MessageSubscription(Protocol):
    @abc.abstractmethod
    def unsubscribe(self) -> None:
        pass
