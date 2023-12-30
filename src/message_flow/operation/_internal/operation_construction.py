from abc import ABCMeta
from typing import TYPE_CHECKING, final

from ...shared import Components, Reference
from ...utils import internal
from .operation_schema import OperationReplySchema, OperationSchema

if TYPE_CHECKING:
    from ..operation import Operation


@final
@internal
class OperationMeta(ABCMeta):
    def __new__(mcs, name, bases, namespace, **kwargs):
        cls: type["Operation"] = super().__new__(mcs, name, bases, namespace, **kwargs)

        def decorated_init(operation_constructor):
            def wrapper(self, *args, **kwargs):
                operation_constructor(self, *args, **kwargs)
                mcs.__post_init__(self)

            return wrapper

        cls.__init__ = decorated_init(cls.__init__)

        return cls

    @staticmethod
    def __post_init__(operation: "Operation") -> None:
        operation.__async_api_reference__ = Reference.for_operation(operation.operation_id)
        operation.__async_api_components__ = Components()

        channel_ref = Reference.for_channel(operation.operation_info["channel"])
        message_ref = channel_ref.merge(operation.message.__async_api_reference__)

        schema = OperationSchema(
            action=operation.action,
            channel=channel_ref.as_link(),
            messages=[message_ref.as_link()],
        )

        if (title := operation.operation_info.get("title")) is not None:
            schema["title"] = title

        if (summary := operation.operation_info.get("summary")) is not None:
            schema["summary"] = summary

        if (description := operation.operation_info.get("description")) is not None:
            schema["description"] = description

        if operation.reply.is_provided and operation.reply.is_valid:
            schema["reply"] = OperationReplySchema(
                channel=Reference.for_channel(operation.reply.channel).as_link(),  # type: ignore
                messages=[operation.reply.message.__async_api_reference__.as_direct_component()],  # type: ignore
            )

        operation.__async_api_components__.add_operation(operation.operation_id, schema)  # type: ignore
