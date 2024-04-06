from types import TracebackType
from typing import Type
from message_flow import MessageFlow, Message, Payload, Header, BaseMiddleware
from message_flow.utils import logger

class OrderCreated(Message):
    order_id: str = Payload()
    tenant_id: str = Header()


class MockMiddleware(BaseMiddleware):
    def on_consume(self) -> None:
        self.headers.update({"a": 123})
        print("h")
        return super().on_consume()
    
    def after_consume(self, error: Exception | None = None) -> None:
        print("11")
        return super().after_consume(error)


class MockMiddleware1(BaseMiddleware):
    def on_consume(self) -> None:
        self.headers.update({"a": 123})
        print("h1")
        return super().on_consume()
    
    def after_consume(self, error: Exception | None = None) -> None:
        print("1122")
        return super().after_consume(error)
    
    def on_produce(self) -> None:
        print("produce")
        return super().on_produce()
    
    def after_produce(self, error: Exception | None = None) -> None:
        print("after produce")
        return super().after_produce(error)


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
app.add_middleware(MockMiddleware)
app.add_middleware(MockMiddleware1)
app.add_middleware(CustomMiddleware)

@app.subscribe(address="orders", message=OrderCreated)
def order_created_handler(order_created: OrderCreated) -> None:
    print("Event received", order_created.order_id, order_created.tenant_id)
    return order_created

app.dispatch()