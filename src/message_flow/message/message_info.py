from typing import Annotated, TypedDict

from typing_extensions import Doc

from ..utils import external
from .correlation_id import CorrelationId
from .message_trait import MessageTrait


@external
class MessageInfo(TypedDict, total=False):
    """
    Declare additional information of the `Message`.

    **Example**

    ```python
    from message_flow import Message, Payload, MessageInfo

    class CreateOrder(Message):
        message_info = MessageInfo(
            title="Create Order",
        )

        product_id: str = Payload()
    ```
    """

    correlation_id: Annotated[
        CorrelationId,
        Doc(
            """
            An object that defines a design-time identifier for message tracing and correlation purposes.

            **Note:** Both *correlation id* attribute and `Header` for it should be defined in the `Message`.

            **Example**

            ```python
            from message_flow import Message, Payload, MessageInfo, CorrelationId, Header

            class CreateOrder(Message):
                message_info = MessageInfo(
                    correlation_id=CorrelationId(location="corelation_id"),
                )

                product_id: str = Payload()
                corelation_id: str = Header()
            ```
            """
        ),
    ]
    title: Annotated[
        str,
        Doc(
            """
            A human-friendly title for the message.

            **Example**

            ```python
            from message_flow import Message, Payload, MessageInfo

            class CreateOrder(Message):
                message_info = MessageInfo(
                    title="Create Order",
                )

                product_id: str = Payload()
            ```
            """
        ),
    ]
    summary: Annotated[
        str,
        Doc(
            """
            A short summary of what the message is about.

            **Example**

            ```python
            from message_flow import Message, Payload, MessageInfo

            class CreateOrder(Message):
                message_info = MessageInfo(
                    summary="Command for order creation.",
                )

                product_id: str = Payload()
            ```
            """
        ),
    ]
    description: Annotated[
        str,
        Doc(
            """
            A verbose explanation of the message. CommonMark syntax can be used for rich text representation.

            **Example**

            ```python
            from message_flow import Message, Payload, MessageInfo

            class CreateOrder(Message):
                message_info = MessageInfo(
                    description="Command for order creation.",
                )

                product_id: str = Payload()
            ```
            """
        ),
    ]
    traits: Annotated[
        list[type[MessageTrait]],
        Doc(
            """
            A list of traits to apply to the message object.

            **Example**

            ```python
            from message_flow import Message, Payload, Header, MessageInfo, CorrelationId, MessageTrait

            
            class CorrelationIdTrait(MessageTrait):
                message_id: str = Header()
                correlation_id = CorrelationId("message_id")


            class CreateOrder(Message):
                message_info = MessageInfo(
                    traits=[CorrelationIdTrait],
                )

                product_id: str = Payload()
            ```
            """
        ),
    ]
