from message_flow import MessageFlow, Message, Payload, Header


class OrderCreated(Message):
    order_id: str = Payload()
    tenant_id: str = Header()


if __name__ == "__main__":
    app = MessageFlow()

    app.publish(OrderCreated(order_id="order_id", tenant_id="tenant_id"), channel_address="orders")
    