from typing import Any, Callable

from ...utils import export
from ..message import Message
from .action_type import ActionType


@export
class Operation:
    def __init__(
        self,
        action: ActionType,
        message: Message,
        handler: Callable[[Message], None] | None = None,
    ) -> None:
        self.action = action
        self.message = message
        self.handler = handler

    def __call__(self, message: Message) -> None:
        if self.handler is None:
            raise RuntimeError(f"Handler not defined for {self.message}")

        self.handler(message)

    @classmethod
    def as_send(cls, message: Message) -> "Operation":
        return cls(action=ActionType.SEND, message=message)

    @classmethod
    def as_receive(cls, message: Message, handler: Any) -> "Operation":
        return cls(action=ActionType.RECEIVE, message=message, handler=handler)

    def handles(self, action_type: ActionType, message_type: str) -> bool:
        return action_type == self.action and message_type == self.message.__name__
