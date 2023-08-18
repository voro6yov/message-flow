from typing import Protocol

from event_flow.utils import export

from ..shared import Message


@export
class MessageProducer(Protocol):
    def send(self, destination: str, message: Message) -> None:
        pass
