import json
from typing import TYPE_CHECKING, Annotated, Any, ClassVar

from pydantic import BaseModel, create_model
from typing_extensions import Doc

from ..shared import Components, Reference
from ..utils import external
from ._internal import MessageMeta
from .header import Header
from .message_info import MessageInfo
from .payload import Payload


@external
class Message(metaclass=MessageMeta):
    """
    Describes a `Message` received on a given `Channel` and `Operation`.

    **Example**

    ```python
    from message_flow import Message, Payload, Header

    class CreateOrder(Message):
        product_id: str = Payload()
        tenant_id: str = Header()
    ```
    """

    if TYPE_CHECKING:
        message_info: ClassVar[MessageInfo]
        __async_api_components__: ClassVar[Components]
        __async_api_reference__: ClassVar[Reference]

    message_info: Annotated[MessageInfo, Doc("Declare additional information of the `Message`.")] = MessageInfo()

    def __str__(self) -> str:
        return f"'<Message> message_id: {self.message_id}'"

    def __repr__(self) -> str:
        return f"'<Message> message_id: {self.message_id}'"

    @property
    def message_id(self) -> str:
        """
        An identifier for the described message.
        """
        return self.__class__.__name__

    @property
    def headers(self) -> dict[str, str]:
        """
        The message headers.

        Returns:
            dict[str, str]: The message headers.
        """
        if not hasattr(self, "_headers"):
            headers_model = self.headers_model()
            self._headers = headers_model(
                **{header_name: getattr(self, header_name) for header_name in self.headers_attributes()}
            ).model_dump()

        return self._headers

    @property
    def payload(self) -> bytes:
        """
        The message payload.

        Returns:
            bytes: The message payload.
        """
        if not hasattr(self, "_payload"):
            payload_model = self.payload_model()
            self._payload = (
                payload_model(
                    **{payload_name: getattr(self, payload_name) for payload_name in self.payload_attributes()}
                )
                .model_dump_json()
                .encode()
            )
        return self._payload

    @classmethod
    def headers_attributes(cls) -> list[str]:
        if not hasattr(cls, "_headers_attributes"):
            cls._headers_attributes = cls._get_attribute_names_for(Header)

        return cls._headers_attributes

    @classmethod
    def payload_attributes(cls) -> list[str]:
        if not hasattr(cls, "_payload_attributes"):
            cls._payload_attributes = cls._get_attribute_names_for(Payload)

        return cls._payload_attributes

    @classmethod
    def headers_model(cls) -> type[BaseModel]:
        """
        Schema definition of the message headers.

        Returns:
            type[BaseModel]: Pydantic model of the message headers.
        """
        if not hasattr(cls, "_headers_model"):
            header_props = (
                (
                    header_name,
                    cls.__annotations__[header_name],
                    cls.__dict__[header_name],
                )
                for header_name in cls.headers_attributes()
            )
            field_definitions = {
                header_name: (
                    Annotated[header_type, header],
                    header.default,
                )
                for header_name, header_type, header in header_props
            }
            cls._headers_model = create_model("headers", **field_definitions)  # type: ignore

        return cls._headers_model

    @classmethod
    def payload_model(cls) -> type[BaseModel]:
        """
        Definition of the message payload.

        Returns:
            type[BaseModel]: Pydantic model of the message payload.
        """
        if not hasattr(cls, "_payload_model"):
            payload_props = (
                (
                    payload_name,
                    cls.__annotations__[payload_name],
                    cls.__dict__[payload_name],
                )
                for payload_name in cls.payload_attributes()
            )
            field_definitions = {
                payload_name: (
                    Annotated[payload_type, payload],
                    payload.default,
                )
                for payload_name, payload_type, payload in payload_props
            }
            cls._payload_model = create_model("payload", **field_definitions)  # type: ignore
        return cls._payload_model

    @classmethod
    def from_payload_and_headers(cls, raw_payload: bytes, raw_headers: dict[str, str]) -> "Message":
        payload_obj = cls.payload_model()(**json.loads(raw_payload.decode()))
        payload: dict[str, Any] = {
            payload_name: getattr(payload_obj, payload_name) for payload_name in cls.payload_attributes()
        }

        headers_obj = cls.headers_model()(**raw_headers)
        headers: dict[str, Any] = {
            header_name: getattr(headers_obj, header_name) for header_name in cls.headers_attributes()
        }
        return cls(**payload, **headers)

    def add_routing_headers(self, extra_headers: dict[str, str]) -> None:
        self.headers.update(extra_headers)

    @classmethod
    def _get_attribute_names_for(cls, attribute_type: type[Header | Payload]) -> list[str]:
        return [
            attribute_name
            for attribute_name in cls.__dict__
            if not attribute_name.startswith("__")
            and not attribute_name.endswith("__")
            and isinstance(cls.__dict__[attribute_name], attribute_type)
        ]
