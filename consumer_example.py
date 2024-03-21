from message_flow import MessageFlow, Message, Payload, Header


class OrderCreated(Message):
    order_id: str = Payload()
    tenant_id: str = Header()


if __name__ == "__main__":
    app = MessageFlow()

    @app.subscribe(address="orders", message=OrderCreated)
    def order_created_handler(order_created: OrderCreated) -> None:
        print("Event received", order_created.order_id, order_created.tenant_id)

    app.dispatch()