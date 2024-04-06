import json
import logging
import warnings
from typing import Annotated, Callable, final

from typing_extensions import Doc, deprecated

from ..channel import Channel
from ..message import Message
from ..utils import external, logger
from ._fast_api import FastAPI
from ._internal import AsyncAPIStudioPage, Channels, Info, MessageFlowSchema
from ._message_management import Dispatcher, Producer
from ._simple_messaging import SimpleMessageConsumer, SimpleMessageProducer
from .base_middleware import BaseMiddleware
from .messaging import MessageConsumer, MessageProducer

MessageHandler = Callable[[Message], Message | None]


@final
@external
class MessageFlow:
    """
    `MessageFlow` app class, the main entrypoint to use MessageFlow.

    **Example**

    ```python
    from message_flow import MessageFlow

    app = MessageFlow()
    ```
    """

    def __init__(
        self,
        *,
        channels: Annotated[
            list[Channel] | None,
            Doc(
                """
                A list of Channels.

                **Example**

                ```python
                from message_flow import MessageFlow, Channel

                order_channel = Channel("order")

                app = MessageFlow(channels=[order_channel])
                ```
                """
            ),
            deprecated(
                """
                You normally wouldn't use this parameter with MessageFlow.

                In MessageFlow, you would normally use the method `add_channel()`
                of the MessageFlow.
                """
            ),
        ] = None,
        message_producer: Annotated[
            MessageProducer | None,
            Doc(
                """
                The message producer to be used for messages producing.

                **Example**

                ```python
                from message_flow import MessageFlow, RabbitMQProducer

                app = MessageFlow(message_consumer=RabbitMQProducer(...))
                ```
                """
            ),
        ] = None,
        message_consumer: Annotated[
            MessageConsumer | None,
            Doc(
                """
                The message consumer to be used for messages consuming.

                **Example**

                ```python
                from message_flow import MessageFlow, RabbitMQConsumer

                app = MessageFlow(message_consumer=RabbitMQConsumer(...))
                ```
                """
            ),
        ] = None,
        title: Annotated[
            str,
            Doc(
                """
                The title of the application.

                It will be added to the generated AsyncAPI.

                **Example**

                ```python
                from message_flow import MessageFlow

                app = MessageFlow(title="MessagingApp")
                ```
                """
            ),
        ] = "MessageFlow",
        version: Annotated[
            str,
            Doc(
                """
                The version of the application API (not to be confused with the specification version).

                It will be added to the generated AsyncAPI.

                **Example**

                ```python
                from message_flow import MessageFlow

                app = MessageFlow(version="0.0.1")
                ```
                """
            ),
        ] = "0.1.0",
        logger: Annotated[
            logging.Logger,
            Doc(
                """
                The custom logger for the application.

                **Example**

                ```python
                import logging
                from message_flow import MessageFlow

                custom_logger = logging.getLogger("custom_logger")

                app = MessageFlow(logger=custom_logger)
                ```
                """
            ),
        ] = logger,
    ) -> None:
        self._logger = logger

        self.asyncapi_version: Annotated[
            str,
            Doc(
                """
                The version string signifies the version of the AsyncAPI 
                Specification that the document complies to.

                MessageFlow will generate AsyncAPI version 3.0.0, and will output that as
                the AsyncAPI version.

                This is not passed as a parameter to the `MessageFlow` class to avoid
                giving the false idea that MessageFlow would generate a different AsyncAPI
                schema. It is only available as an attribute.

                **Example**

                ```python
                from message_flow import MessageFlow

                app = MessageFlow()

                app.asyncapi_version = "3.0.2"
                ```
                """
            ),
        ] = "3.0.0"
        self.title = title
        self.version = version

        self._channels = Channels(channels=channels)
        self._message_producer = message_producer or SimpleMessageProducer(self._logger)
        self._message_consumer = message_consumer or SimpleMessageConsumer(self._logger)

    @property
    def producer(self) -> Producer:
        if not hasattr(self, "_producer"):
            self._producer = Producer(self._message_producer)
        return self._producer

    @property
    def dispatcher(self) -> Dispatcher:
        if not hasattr(self, "_dispatcher"):
            self._dispatcher = Dispatcher(self._channels, self._message_consumer, self.producer, self._logger)
        return self._dispatcher

    def add_channel(self, channel: Annotated[Channel, Doc("The channel to add.")]) -> None:
        """
        Add an `Channel` in the same app.

        **Example**

        ```python
        from message_flow import MessageFlow

        from .orders import order_channel

        app = MessageFlow()

        app.add_channel(order_channel)
        ```
        """
        self._channels.include_channel(channel)

    def publish(
        self,
        message: Annotated[Message, Doc("The message to publish.")],
        *,
        channel_address: Annotated[
            str | None,
            Doc(
                """
                The address to which channel the message should be published.

                **Note**: Has lower priority than added channel.

                **Example**

                ```python title="Publishing without channel addition"
                from message_flow import MessageFlow

                from .orders import OrderCreated

                app = MessageFlow()

                app.publish(OrderCreated(order_id="order_id"), channel_address="orders")
                ```
                """
            ),
        ] = None,
    ) -> None:
        """
        Publish `Message` to the added `Channel` or to the specified *channel address*.

        Added `Channel` has higher priority than specified `channel address`.

        **Example**

        ```python title="Publishing with channel addition"
        from message_flow import MessageFlow

        from .orders import order_channel, OrderCreated

        app = MessageFlow()

        app.add_channel(order_channel)
        app.publish(OrderCreated(order_id="order_id"))
        ```

        Raises:
            RuntimeError: Raised when channel is not found for given message
                and channel address is not provided explicitly.
        """
        if (channel := self._channels.channel_of(message)) is None and channel_address is None:
            raise RuntimeError(f"Could not find channel for {message}")

        self.producer.send(
            channel=channel.address if channel is not None else channel_address,  # type: ignore
            message=message,
        )

    def send(
        self,
        message: Annotated[Message, Doc("The message to send.")],
        *,
        channel_address: Annotated[
            str | None,
            Doc(
                """
                The address to which channel the message should be sent.

                **Note**: Has lower priority than added channel.

                **Example**

                ```python title="Sending without channel addition"
                from message_flow import MessageFlow

                from .orders import CreateOrder

                app = MessageFlow()

                app.send(
                    CreateOrder(product_id="product_id", amount=1), 
                    channel_address="orders"
                )
                ```
                """
            ),
        ] = None,
        reply_to_address: Annotated[
            str | None,
            Doc(
                """
                The reply address to which channel the message should be sent by consumer.

                **Note**: Has lower priority than added operation's reply channel.

                **Example**

                ```python title="Sending without channel addition with reply address"
                from message_flow import MessageFlow

                from .orders import CreateOrder

                app = MessageFlow()

                app.send(
                    CreateOrder(product_id="product_id", amount=1), 
                    channel_address="orders", 
                    reply_to_address="orders_reply"
                )
                ```
                """
            ),
        ] = None,
    ) -> None:
        """
        Send `Message` to the added `Channel` or to the specified *channel address*.
        Also, reply address can be provided.

        Added `Channel` has higher priority than specified `channel address`
        and reply address defined in the operation has higher priority than specified
        `reply address`

        **Example**

        ```python title="Sending with channel addition"
        from message_flow import MessageFlow

        from .orders import order_channel, CreateOrder

        app = MessageFlow()

        app.add_channel(order_channel)
        app.send(CreateOrder(product_id="product_id", amount=1))
        ```

        Raises:
            RuntimeError: Raised when channel is not found for given message
                and channel address is not provided explicitly.
        """
        channel, operation = self._channels.channel_and_operation_of(message) or (None, None)

        if channel is None and channel_address is None:
            raise RuntimeError(f"Could not find channel for {message}")

        self.producer.send(
            channel=channel.address if channel is not None else channel_address,  # type: ignore
            message=message,
            reply_to_address=operation.reply.channel if operation is not None else reply_to_address,
        )

    def subscribe(
        self,
        address: Annotated[str, Doc("The `Channel` address.")],
        message: Annotated[type[Message], Doc("The type of `Message`s that will be consumed on the channel.")],
    ) -> Callable[[MessageHandler], MessageHandler]:
        """
        Subscribe to `Message` from the `Channel` with specified *address*.

        **Note:** If the Channel was not explicitly added to the app, it will
        be implicitly added.

        **Example**

        ```python title="Subscribing to messages from the channel"
        from message_flow import MessageFlow

        from .orders import OrderCreated

        app = MessageFlow()

        @app.subscribe(address="orders", message=OrderCreated)
        def handle_order_created(event: OrderCreated) -> None:
            ...
        ```

        Returns:
            Callable[[MessageHandler], MessageHandler]: "Decorated handler used for `Message` processing."
        """
        channel = self._channels.find_or_create_for(address)
        return channel.subscribe(message)

    def dispatch(self) -> None:
        """
        Initiate the dispatch of `Messages` on the added `Channels`.

        **Example**

        ```python title="Starting dispatching"
        from message_flow import MessageFlow

        from .orders import OrderCreated

        app = MessageFlow()

        @app.subscribe(address="orders", message=OrderCreated)
        def handle_order_created(event: OrderCreated) -> None:
            ...

        app.dispatch()
        ```
        """
        try:
            self.dispatcher.initialize()
            self._logger.info("Message Flow app starting...")
            self._message_consumer.start_consuming()
        except Exception as error:
            self._logger.error("An error occurred while dispatching events", exc_info=error)
            raise
        finally:
            self._message_consumer.close()
            self._message_producer.close()

    def make_async_api_schema(self) -> str:
        """
        Generate AsyncAPI schema for the specified `Channels`, `Operations` and `Messages`.

        **Example**

        ```python title="Making AsyncAPI Schema"
        from message_flow import MessageFlow

        from .orders import OrderCreated

        app = MessageFlow()

        @app.subscribe(address="orders", message=OrderCreated)
        def handle_order_created(event: OrderCreated) -> None:
            ...

        app.make_async_api_schema()
        ```

        Returns:
            str: Generated AsyncAPI schema.
        """
        schema = MessageFlowSchema(
            asyncapi=self.asyncapi_version,
            info=Info(title=self.title, version=self.version),
            channels=self._channels.channels_schema,
            operations=self._channels.operations_schema,
            components=self._channels.components,
        )

        return json.dumps(schema)

    def generate_docs_page(
        self,
        title: Annotated[str, Doc("The AsyncAPI Studio page title.")] = "MessageFlow",
        sidebar: Annotated[bool, Doc("Show sidebar flag.")] = True,
        info: Annotated[bool, Doc("Show info flag.")] = True,
        servers: Annotated[bool, Doc("Show servers flag.")] = True,
        operations: Annotated[bool, Doc("Show operations flag.")] = True,
        messages: Annotated[bool, Doc("Show messages flag.")] = True,
        schemas: Annotated[bool, Doc("Show schemas flag.")] = True,
        errors: Annotated[bool, Doc("Show errors flag.")] = True,
    ) -> str:
        """
        Generate AsyncAPI Studio page for the generated AsyncAPI schema.

        **Example**

        ```python title="Generating AsyncAPI Studio Page"
        from message_flow import MessageFlow

        from .orders import OrderCreated

        app = MessageFlow()

        @app.subscribe(address="orders", message=OrderCreated)
        def handle_order_created(event: OrderCreated) -> None:
            ...

        app.generate_docs_page()
        ```

        Returns:
            str: Generated AsyncAPI Studio page.
        """
        return AsyncAPIStudioPage(
            schema=self.make_async_api_schema(),
            title=title,
            sidebar=sidebar,
            info=info,
            servers=servers,
            operations=operations,
            messages=messages,
            schemas=schemas,
            errors=errors,
        ).generate()

    def set_logging_level(self, level: Annotated[int, Doc("Logging level to set.")]) -> None:
        """
        Set logging level for the app logger.

        **Example**

        ```python title="Setting logging level"
        import logging

        from message_flow import MessageFlow

        app = MessageFlow()

        app.set_logging_level(logging.INFO)
        ```
        """
        self._logger.setLevel(level=level)

    def add_async_api_documentation(
        self,
        fast_api: Annotated[FastAPI, Doc("FastAPI app.")],
        documentation_url: Annotated[
            str, Doc("URL of the AsyncAPI Studio page in the FastAPI app.")
        ] = "/async-api-docs",
    ) -> None:
        """
        Add AsyncAPI documentation page to the FastAPI application.

        **Example**

        ```python title="Adding AsyncAPI Studio page to FastAPI"
        from message_flow import MessageFlow
        from fastapi import FastAPI

        app = MessageFlow()
        fast_api_app = FastAPI()

        app.add_async_api_documentation(fast_api_app)
        ```
        """
        try:
            from fastapi import Request  # pyright: ignore[reportMissingImports]
            from fastapi.responses import HTMLResponse  # pyright: ignore[reportMissingImports]
        except ImportError:
            warnings.warn("Please use this method only with FastAPI installed.")
            return

        documentation_page = self.generate_docs_page()

        async def async_api_docs_html(req: Request) -> HTMLResponse:
            return HTMLResponse(documentation_page)

        fast_api.add_route(documentation_url, async_api_docs_html, include_in_schema=False)

    def add_middleware(
        self, middleware: Annotated[type[BaseMiddleware], Doc("Message processing Middleware.")]
    ) -> None:
        """
        Add Middleware.

        **Example**

        ```python title="Adding processing Middleware"
        import logging
        from message_flow import MessageFlow, BaseMiddleware

        logger = logging.getLogger(__name__)


        class CustomMiddleware(BaseMiddleware):
            def on_consume(self) -> None:
                logger.info("Message with %s payload and %s headers received.", self.payload, self.headers)
                return super().on_consume()

            def after_consume(self, error: Exception | None = None) -> None:
                logger.info("Message with %s payload and %s headers processed.", self.payload, self.headers)
                return super().after_consume(error)

            def on_produce(self) -> None:
                logger.info("Producing message with %s payload and %s headers.", self.payload, self.headers)
                return super().on_produce()

            def after_produce(self, error: Exception | None = None) -> None:
                logger.info("Message with %s payload and %s headers produced.", self.payload, self.headers)
                return super().after_produce(error)

        app = MessageFlow()
        app.add_middleware(CustomMiddleware)

        ```
        """
        self.dispatcher.add_middleware(middleware=middleware)
