from typing import Annotated, ClassVar

from typing_extensions import Doc

from ..utils import external


@external
class MessageExample:
    """
    `Message Example` represents an example of a `Message`.

    **Example**

    ```python
    from message_flow import MessageExample


    class OrderCreatedExample(MessageExample):
        order_id = "some_order_id"
        product_id = "some_product_id"
    ```
    """

    name: Annotated[
        ClassVar[str],
        Doc(
            """
            A machine-friendly name.

            **Example**

            ```python
            from message_flow import MessageExample

            
            class OrderCreatedExample(MessageExample):
                name="OrderCreated"
            ```
            """
        ),
    ]
    summary: Annotated[
        ClassVar[str],
        Doc(
            """
            A short summary of what the example is about.

            **Example**

            ```python
            from message_flow import MessageExample

            
            class OrderCreated(MessageExample):
                name="OrderCreated"
            ```
            """
        ),
    ]
