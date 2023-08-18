from typing import Protocol

from event_flow.utils import export

from ..shared import Message


@export
class MessageHandler(Protocol):
    def __call__(self, message: Message) -> None:
        pass
