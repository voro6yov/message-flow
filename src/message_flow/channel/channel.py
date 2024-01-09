from typing import TYPE_CHECKING, Annotated, Callable, final

from typing_extensions import Doc

from ..message import Message
from ..operation import Operation
from ..shared import Components, Reference
from ..utils import external
from ._internal import ChannelInfo, ChannelMeta

MessageHandler = Callable[[Message], Message | None]


@final
@external
class Channel(metaclass=ChannelMeta):
    """
    Describes a shared communication `Channel`.

    **Example**

    ```python
    from message_flow import Channel

    orders = Channel()
    ```
    """

    if TYPE_CHECKING:
        _messages: dict[str, dict[str, str]]
        __async_api_components__: Components
        __async_api_reference__: Reference

    def __init__(
        self,
        address: Annotated[
            str | None,
            Doc(
                """
                The string representation of this `Channel's` address. The address 
                is typically the "topic name", "routing key", "event type", or "path".

                **Note:** When null or absent, it will be interpreted as *unknown*. 
                This is useful when the address is generated dynamically at runtime 
                or can't be known upfront.

                **Example**

                ```python
                from message_flow import Channel

                orders = Channel("orders")
                ```
                """
            ),
        ] = None,
        *,
        title: Annotated[
            str | None,
            Doc(
                """
                A human-friendly title for the channel.

                It will be added to the generated AsyncAPI.

                **Example**

                ```python
                from message_flow import Channel

                orders = Channel("orders", title="Orders Channel")
                ```
                """
            ),
        ] = None,
        summary: Annotated[
            str | None,
            Doc(
                """
                A short summary of the channel.

                It will be added to the generated AsyncAPI.

                **Example**

                ```python
                from message_flow import Channel

                orders = Channel("orders", summary="Used to send order messages.")
                ```
                """
            ),
        ] = None,
        description: Annotated[
            str | None,
            Doc(
                """
                A description of this channel. CommonMark syntax can be used for 
                rich text representation.

                It will be added to the generated AsyncAPI.

                **Example**

                ```python
                from message_flow import Channel

                orders = Channel("orders", description="Used to send order messages.")
                ```
                """
            ),
        ] = None,
    ) -> None:
        self.address = address or "unknown"

        self.channel_info = self._make_channel_info(
            title=title,
            summary=summary,
            description=description,
        )

        self.operations: Annotated[list[Operation], Doc("`Operations` added to the `Channel`.")] = []

    @property
    def channel_id(self) -> str:
        """
        An identifier for the described channel.
        """
        return self.address

    def publish(
        self,
        *,
        title: Annotated[
            str | None,
            Doc(
                """
                A human-friendly title for the operation.

                It will be added to the generated AsyncAPI.

                **Example**

                ```python
                from message_flow import Channel, Message, Payload

                orders_channel = Channel("orders")

                @orders_channel.publish(title="Order Created.")
                class OrderCreated(Message):
                    order_id: str = Payload()
                ```
                """
            ),
        ] = None,
        summary: Annotated[
            str | None,
            Doc(
                """
                A short summary of what the operation is about.

                It will be added to the generated AsyncAPI.

                **Example**

                ```python
                from message_flow import Channel, Message, Payload

                orders_channel = Channel("orders")

                @orders_channel.publish(summary="Used to publish Order Created events.")
                class OrderCreated(Message):
                    order_id: str = Payload()
                ```
                """
            ),
        ] = None,
        description: Annotated[
            str | None,
            Doc(
                """
                A verbose explanation of the operation. CommonMark syntax can be 
                used for rich text representation.

                It will be added to the generated AsyncAPI.

                **Example**

                ```python
                from message_flow import Channel, Message, Payload

                orders_channel = Channel("orders")

                @orders_channel.publish(description="Used to publish Order Created events.")
                class OrderCreated(Message):
                    order_id: str = Payload()
                ```
                """
            ),
        ] = None,
    ) -> Callable[[type[Message]], type[Message]]:
        """
        Add event publishing operation using a *send* `Operation`.

        **Example**

        ```python
        from message_flow import Channel, Message, Payload

        orders_channel = Channel("orders")

        @orders_channel.publish()
        class OrderCreated(Message):
            order_id: str = Payload()
        ```

        Returns:
            Callable[[type[Message]], type[Message]]: Decorated message.
        """

        def decorator(message: type[Message]) -> type[Message]:
            self._add_message(message)  # type: ignore
            self._add_operation(  # type: ignore
                Operation.as_event(
                    message,
                    channel=self.channel_id,
                    title=title,
                    summary=summary,
                    description=description,
                )
            )

            return message

        return decorator

    def send(
        self,
        reply: Annotated[
            type[Message] | None,
            Doc(
                """
                The `Message` type that can be processed by this operation as reply.

                **Note:** Both *reply* and *reply channel* should be provided simultaneously.

                ```python title="Sending a command that requires a reply."
                from message_flow import Channel, Message, Payload
                from orders_reply import CreateOrderReply, orders_reply_channel

                orders_channel = Channel("orders")

                @orders_channel.send(reply=CreateOrderReply, reply_channel=orders_reply_channel)
                class CreateOrder(Message):
                    order_id: str = Payload()
                ```
                """
            ),
        ] = None,
        reply_channel: Annotated[
            "Channel | None",
            Doc(
                """
                The `Channel` in which this operation is performed.

                **Note:** Both *reply* and *reply channel* should be provided simultaneously.

                **Example**

                ```python title="Sending a command that requires a reply."
                from message_flow import Channel, Message, Payload
                from orders_reply import CreateOrderReply, orders_reply_channel

                orders_channel = Channel("orders")

                @orders_channel.send(reply=CreateOrderReply, reply_channel=orders_reply_channel)
                class CreateOrder(Message):
                    order_id: str = Payload()
                ```
                """
            ),
        ] = None,
        *,
        title: Annotated[
            str | None,
            Doc(
                """
                A human-friendly title for the operation.

                It will be added to the generated AsyncAPI.

                **Example**

                ```python
                from message_flow import Channel, Message, Payload

                orders_channel = Channel("orders")

                @orders_channel.send(title="Create Order.")
                class CreateOrder(Message):
                    order_id: str = Payload()
                ```
                """
            ),
        ] = None,
        summary: Annotated[
            str | None,
            Doc(
                """
                A short summary of what the operation is about.

                It will be added to the generated AsyncAPI.

                **Example**

                ```python
                from message_flow import Channel, Message, Payload

                orders_channel = Channel("orders")

                @orders_channel.send(summary="Used to send Create Order commands.")
                class CreateOrder(Message):
                    order_id: str = Payload()
                ```
                """
            ),
        ] = None,
        description: Annotated[
            str | None,
            Doc(
                """
                A verbose explanation of the operation. CommonMark syntax can be 
                used for rich text representation.

                It will be added to the generated AsyncAPI.

                **Example**

                ```python
                from message_flow import Channel, Message, Payload

                orders_channel = Channel("orders")

                @orders_channel.send(description="Used to send Create Order commands.")
                class CreateOrder(Message):
                    order_id: str = Payload()
                ```
                """
            ),
        ] = None,
    ) -> Callable[[type[Message]], type[Message]]:
        """
        Add command sending operation using a *send* `Operation`.

        **Example**

        ```python title="Sending a command without requiring a reply."
        from message_flow import Channel, Message, Payload

        orders_channel = Channel("orders")

        @orders_channel.send()
        class CreateOrder(Message):
            order_id: str = Payload()
        ```

        Raises:
            RuntimeError: Raises when only reply or reply channel address is provided.

        Returns:
            Callable[[type[Message]], type[Message]]: Decorated message.
        """

        def decorator(message: type[Message]) -> type[Message]:
            self._add_message(message)  # type: ignore
            self._add_operation(  # type: ignore
                Operation.as_command(
                    message,
                    reply,
                    reply_channel.channel_id if reply_channel is not None else None,
                    channel=self.channel_id,
                    title=title,
                    summary=summary,
                    description=description,
                )
            )

            return message

        return decorator

    def subscribe(
        self,
        message: Annotated[type[Message], Doc("The `Message` type that can be processed by this operation.")],
        *,
        title: Annotated[
            str | None,
            Doc(
                """
                A human-friendly title for the operation.

                It will be added to the generated AsyncAPI.

                **Example**

                ```python
                from message_flow import Channel, Message, Payload

                orders_channel = Channel("orders")

                class OrderCreated(Message):
                    order_id: str = Payload()

                @orders_channel.subscribe(OrderCreated, title="Order Created handler.")
                def handle_order_created(message: OrderCreated) -> None:
                    ...
                ```
                """
            ),
        ] = None,
        summary: Annotated[
            str | None,
            Doc(
                """
                A short summary of what the operation is about.

                It will be added to the generated AsyncAPI.

                **Example**

                ```python
                from message_flow import Channel, Message, Payload

                orders_channel = Channel("orders")

                class OrderCreated(Message):
                    order_id: str = Payload()

                @orders_channel.subscribe(OrderCreated, summary="Used to handle Order Created event.")
                def handle_order_created(message: OrderCreated) -> None:
                    ...
                ```
                """
            ),
        ] = None,
        description: Annotated[
            str | None,
            Doc(
                """
                A verbose explanation of the operation. CommonMark syntax can be 
                used for rich text representation.

                It will be added to the generated AsyncAPI.

                **Example**

                ```python
                from message_flow import Channel, Message, Payload

                orders_channel = Channel("orders")

                class OrderCreated(Message):
                    order_id: str = Payload()

                @orders_channel.subscribe(OrderCreated, description="Used to handle Order Created event.")
                def handle_order_created(message: OrderCreated) -> None:
                    ...
                ```
                """
            ),
        ] = None,
    ) -> Callable[[MessageHandler], MessageHandler]:
        """
        Add subscribe operation using a *receive* `Operation`.

        **Example**

        ```python
        from message_flow import Channel, Message, Payload

        orders_channel = Channel("orders")

        class OrderCreated(Message):
            order_id: str = Payload()

        @orders_channel.subscribe(OrderCreated)
        def handle_order_created(message: OrderCreated) -> None:
            ...
        ```

        Returns:
            Callable[[MessageHandler], MessageHandler]: Decorated message handler.
        """

        def decorator(handler: MessageHandler) -> MessageHandler:
            self._add_message(message)  # type: ignore
            self._add_operation(  # type: ignore
                Operation.as_subscription(
                    message,
                    handler,
                    channel=self.channel_id,
                    title=title,
                    summary=summary,
                    description=description,
                )
            )

            return handler

        return decorator

    def sends(self, message_id: Annotated[str, Doc("The argument represents the message identifier.")]) -> bool:
        """
        Check is `Channel` has *send* `Operation` for given `Message`.

        Returns:
            bool: Check result.
        """
        return (
            next(
                filter(lambda o: o.sends(message_id), self.operations),
                None,
            )
            is not None
        )

    def receives(
        self,
        address: Annotated[str, Doc("The string representation of the `Channel's` address")],
        message_id: Annotated[str, Doc("The argument represents the message identifier.")],
    ) -> Operation | None:
        """
        Check is `Channel` has *receive* `Operation` for given *address* and `Message`.

        Returns:
            bool: Check result.
        """
        return next(
            filter(
                lambda o: address == self.address and o.receives(message_id),
                self.operations,
            ),
            None,
        )

    def _make_channel_info(
        self,
        title: str | None,
        summary: str | None,
        description: str | None,
    ) -> ChannelInfo:
        channel_info = ChannelInfo()
        if title is not None:
            channel_info["title"] = title
        if summary is not None:
            channel_info["summary"] = summary
        if description is not None:
            channel_info["description"] = description

        return channel_info
