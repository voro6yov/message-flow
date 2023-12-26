from typing import Any, final

from ..utils import internal


@final
@internal
class Components:
    def __init__(self) -> None:
        self.schemas: dict[str, Any] = {}
        self.channels: dict[str, Any] = {}
        self.operations: dict[str, Any] = {}
        self.messages: dict[str, Any] = {}

    def add_schemas(self, schemas: dict[str, Any]) -> None:
        self.schemas.update(schemas)

    def add_channel(self, channel_id: str, channel: dict[str, Any]) -> None:
        self.channels[channel_id] = channel

    def add_operation(self, operation_id: str, operation: dict[str, Any]) -> None:
        self.operations[operation_id] = operation

    def add_message(self, message_id: str, message: dict[str, Any]) -> None:
        self.messages[message_id] = message

    def merge(self, components: "Components") -> None:
        self.schemas.update(components.schemas)
        self.channels.update(components.channels)
        self.operations.update(components.operations)
        self.messages.update(components.messages)

    def as_schema(self) -> dict[str, Any]:
        return {
            "schemas": self.schemas,
            "channels": self.channels,
            "operations": self.operations,
            "messages": self.messages,
        }
