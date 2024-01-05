from typing import Any, final

from ...channel import Channel
from ...message import Message
from ...operation import Operation
from ...shared import Components
from ...utils import internal


@final
@internal
class Channels:
    def __init__(self, *, channels: list[Channel] | None = None) -> None:
        self._channels: list[Channel] = channels or []

    @property
    def addresses(self) -> set[str]:
        if not hasattr(self, "_addresses"):
            self._addresses = {channel.address for channel in self._channels}

        return self._addresses

    @property
    def channels_schema(self) -> dict[str, dict[str, str]]:
        if not hasattr(self, "_channels_schema"):
            self._make_schemas()

        return self._channels_schema

    @property
    def operations_schema(self) -> dict[str, dict[str, str]]:
        if not hasattr(self, "_operations_schema"):
            self._make_schemas()

        return self._operations_schema

    @property
    def components(self) -> dict[str, Any]:
        if not hasattr(self, "_components"):
            self._make_schemas()

        return self._components.as_schema()

    def include_channel(self, channel: Channel) -> None:
        self._channels.append(channel)

    def channel_of(self, message: Message) -> Channel | None:
        return next(filter(lambda c: c.sends(message.message_id), self._channels), None)

    def operation_of(self, address: str, message_id: str) -> Operation | None:
        for channel in self._channels:
            if (operation := channel.receives(address, message_id)) is not None:
                return operation

    def channel_and_operation_of(self, message: Message) -> tuple[Channel, Operation] | None:
        for channel in self._channels:
            for operation in channel.operations:
                if operation.sends(message.message_id):
                    return channel, operation

    def find_or_create_for(self, address: str) -> Channel:
        if (channel := next(filter(lambda c: c.address == address, self._channels), None)) is None:
            channel = Channel(address)
            self._channels.append(channel)

        return channel

    def _make_schemas(self) -> None:
        self._channels_schema = {}
        self._operations_schema = {}
        self._components = Components()

        for channel in self._channels:
            self._channels_schema.update(channel.__async_api_reference__.as_component())
            for operation in channel.operations:
                self._operations_schema.update(operation.__async_api_reference__.as_component())

            self._components.merge(channel.__async_api_components__)
