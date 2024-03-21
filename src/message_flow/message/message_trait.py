from typing import TYPE_CHECKING, Annotated, Any, ClassVar

from typing_extensions import Doc

from ..utils import external
from .correlation_id import CorrelationId
from .header import Header

if TYPE_CHECKING:
    from .message_info import MessageInfo


@external
class MessageTrait:
    """
    Describes a trait that MAY be applied to a `Message`. This object may
    contain any property from the `Message`, except payload and traits.

    **Example**

    ```python
    from message_flow import Header, CorrelationId, MessageTrait


    class CorrelationIdTrait(MessageTrait):
        message_id: str = Header()
        correlation_id = CorrelationId("message_id")
    ```
    """

    correlation_id: Annotated[
        ClassVar[CorrelationId],
        Doc(
            """
            Definition of the correlation ID used for message tracing or matching.

            **Example**

            ```python
            from message_flow import CorrelationId, MessageTrait

            
            class CorrelationIdTrait(MessageTrait):
                correlation_id=CorrelationId("message_id")
            ```
            """
        ),
    ]
    title: Annotated[
        ClassVar[str],
        Doc(
            """
            A human-friendly title for the message.

            **Example**

            ```python
            from message_flow import MessageTrait

            
            class InfoTrait(MessageTrait):
                title="Create Order"
            ```
            """
        ),
    ]
    summary: Annotated[
        ClassVar[str],
        Doc(
            """
            A short summary of what the message is about.

            **Example**

            ```python
            from message_flow import MessageTrait

            
            class InfoTrait(MessageTrait):
                summary="Used to create orders"
            ```
            """
        ),
    ]
    description: Annotated[
        ClassVar[str],
        Doc(
            """
            A verbose explanation of the message. CommonMark syntax can be used for rich text representation.

            **Example**

            ```python
            from message_flow import MessageTrait

            
            class InfoTrait(MessageTrait):
                description="Used to create orders"
            ```
            """
        ),
    ]

    @classmethod
    def update_headers(cls, namespace: dict[str, Any]) -> None:
        for header_name, header in cls.headers_attributes().items():
            if header_name not in namespace:
                namespace[header_name] = header
                namespace["__annotations__"][header_name] = cls.__annotations__[header_name]

    @classmethod
    def update_message_info(cls, namespace: dict[str, Any]) -> None:
        message_info: MessageInfo = namespace["message_info"]

        if hasattr(cls, "correlation_id") and message_info.get("correlation_id") is None:
            message_info["correlation_id"] = cls.correlation_id

        if hasattr(cls, "title") and message_info.get("title") is None:
            message_info["title"] = cls.title

        if hasattr(cls, "summary") and message_info.get("summary") is None:
            message_info["summary"] = cls.summary

        if hasattr(cls, "description") and message_info.get("description") is None:
            message_info["description"] = cls.description

    @classmethod
    def headers_attributes(cls) -> dict[str, Header]:
        if not hasattr(cls, "_headers_attributes"):
            cls._headers_attributes = {
                header_name: cls.__dict__[header_name] for header_name in cls._get_attribute_names_for(Header)
            }

        return cls._headers_attributes

    @classmethod
    def _get_attribute_names_for(cls, attribute_type: type[Header]) -> list[str]:
        return [
            attribute_name
            for attribute_name in cls.__dict__
            if not attribute_name.startswith("__")
            and not attribute_name.endswith("__")
            and isinstance(cls.__dict__[attribute_name], attribute_type)
        ]
