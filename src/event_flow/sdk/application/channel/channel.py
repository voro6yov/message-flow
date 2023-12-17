from typing import Callable

from ...utils import export
from ..message import Message
from .action_type import ActionType
from .operation import Operation

EventHandler = Callable[[Message], None]


@export
class Channel:
    def __init__(self, address: str) -> None:
        self.address = address

        self._operations: list[Operation] = []

    def publish(self) -> Callable[[Message], Message]:
        def decorator(message: Message) -> Message:
            self._operations.append(Operation.as_send(message))

            return message

        return decorator

    def subscribe(self, message: Message) -> Callable[[EventHandler], EventHandler]:
        def decorator(handler: EventHandler) -> EventHandler:
            self._operations.append(Operation.as_receive(message, handler))

            return handler

        return decorator

    def sends(self, message: Message) -> bool:
        return next(filter(lambda o: o.handles(ActionType.SEND, message.type), self._operations), None) is not None

    def find_operation(self, address: str, message_type: str) -> Operation | None:
        return next(
            filter(lambda o: address == self.address and o.handles(ActionType.RECEIVE, message_type), self._operations),
            None,
        )
