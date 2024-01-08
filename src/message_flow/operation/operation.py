from typing import TYPE_CHECKING, Any, Callable, final

from ..message import Message
from ..shared import Components, Reference
from ..utils import internal
from ._internal import OperationInfo, OperationMeta
from .action_type import ActionType
from .operation_reply import OperationReply


@final
@internal
class Operation(metaclass=OperationMeta):
    if TYPE_CHECKING:
        __async_api_components__: Components
        __async_api_reference__: Reference

    def __init__(
        self,
        action: str,
        message: type[Message],
        reply: type[Message] | None = None,
        reply_channel: str | None = None,
        handler: Callable[[Message], Message | None] | None = None,
        *,
        channel: str,
        title: str | None,
        summary: str | None,
        description: str | None,
    ) -> None:
        self.action = action
        self.message = message
        self.reply = OperationReply(message=reply, channel=reply_channel)
        self.handler = handler

        if not self.reply.is_valid:
            raise RuntimeError("You should provide both reply and reply channel address.")

        self.operation_info = self._make_operation_info(
            channel=channel,
            title=title,
            summary=summary,
            description=description,
        )

    def __call__(self, message: Message) -> Message | None:
        if self.handler is None:
            raise RuntimeError(f"Handler not defined for {self.message}")

        return self.handler(message)

    @property
    def operation_id(self) -> str:
        return f"{self.action}{self.message.__name__}"

    @classmethod
    def as_event(
        cls,
        message: type[Message],
        *,
        channel: str,
        title: str | None = None,
        summary: str | None = None,
        description: str | None = None,
    ) -> "Operation":
        return cls(
            action=ActionType.SEND,
            message=message,
            channel=channel,
            title=title,
            summary=summary,
            description=description,
        )

    @classmethod
    def as_command(
        cls,
        message: type[Message],
        reply: type[Message] | None,
        reply_channel: str | None,
        *,
        channel: str,
        title: str | None = None,
        summary: str | None = None,
        description: str | None = None,
    ) -> "Operation":
        return cls(
            action=ActionType.SEND,
            message=message,
            reply=reply,
            reply_channel=reply_channel,
            channel=channel,
            title=title,
            summary=summary,
            description=description,
        )

    @classmethod
    def as_subscription(
        cls,
        message: type[Message],
        handler: Any,
        *,
        channel: str,
        title: str | None = None,
        summary: str | None = None,
        description: str | None = None,
    ) -> "Operation":
        return cls(
            action=ActionType.RECEIVE,
            message=message,
            handler=handler,
            channel=channel,
            title=title,
            summary=summary,
            description=description,
        )

    def sends(self, message_id: str) -> bool:
        return ActionType.SEND == self.action and message_id == self.message.__name__

    def receives(self, message_id: str) -> bool:
        return ActionType.RECEIVE == self.action and message_id == self.message.__name__

    def _make_operation_info(
        self,
        channel: str,
        title: str | None,
        summary: str | None,
        description: str | None,
    ) -> OperationInfo:
        operation_info = OperationInfo(channel=channel)

        if title is not None:
            operation_info["title"] = title
        if summary is not None:
            operation_info["summary"] = summary
        if description is not None:
            operation_info["description"] = description

        return operation_info
