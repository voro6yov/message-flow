from abc import ABCMeta
from typing import TYPE_CHECKING

from ...message import Message
from ...operation import Operation
from ...shared import Components, Reference
from ...utils import internal
from .channel_schema import ChannelSchema

if TYPE_CHECKING:
    from ..channel import Channel


@internal
class ChannelMeta(ABCMeta):
    def __new__(mcs, name, bases, namespace, **kwargs):
        cls: type["Channel"] = super().__new__(mcs, name, bases, namespace, **kwargs)

        def decorated_init(channel_constructor):
            def wrapper(self, *args, **kwargs):
                channel_constructor(self, *args, **kwargs)
                mcs.__post_init__(self)

            return wrapper

        cls.__init__ = decorated_init(cls.__init__)
        cls._add_message = mcs._add_message
        cls._add_operation = mcs._add_operation

        return cls

    @staticmethod
    def __post_init__(channel: "Channel") -> None:
        channel._messages = {}

        channel.__async_api_reference__ = Reference.for_channel(channel.channel_id)
        channel.__async_api_components__ = Components()

        schema = ChannelSchema(
            address=channel.address,
            messages=channel._messages,
        )

        if (title := channel.channel_info.get("title")) is not None:
            schema["title"] = title

        if (summary := channel.channel_info.get("summary")) is not None:
            schema["summary"] = summary

        if (description := channel.channel_info.get("description")) is not None:
            schema["description"] = description

        channel.__async_api_components__.add_channel(channel.channel_id, schema)  # type: ignore

    @staticmethod
    def _add_message(channel: "Channel", message: type[Message]) -> None:
        channel._messages.update(message.__async_api_reference__.as_component())
        channel.__async_api_components__.merge(message.__async_api_components__)

    @staticmethod
    def _add_operation(channel: "Channel", operation: Operation) -> None:
        channel.operations.append(operation)
        channel.__async_api_components__.merge(operation.__async_api_components__)
