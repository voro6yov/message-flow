from typing import TYPE_CHECKING, Any, ClassVar

from ..utils import external
from .correlation_id import CorrelationId
from .header import Header

if TYPE_CHECKING:
    from .message_info import MessageInfo


@external
class MessageTrait:
    """
    Describes a trait that MAY be applied to a Message Object. This object MAY
    contain any property from the Message Object, except payload and traits.
    """

    correlation_id: ClassVar[CorrelationId]
    title: ClassVar[str]
    summary: ClassVar[str]
    description: ClassVar[str]

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
