# Message Flow

[![CI](https://github.com/voro6yov/message-flow/actions/workflows/ci.yml/badge.svg?event=push&branch=main)](https://github.com/voro6yov/message-flow/actions/workflows/ci.yml?query=branch%3Amain+event%3Apush)
[![Coverage](https://coverage-badge.samuelcolvin.workers.dev/voro6yov/message-flow.svg)](https://github.com/voro6yov/message-flow/actions?query=event%3Apush+branch%3Amain+workflow%3ACI)<br>
[![pypi](https://img.shields.io/pypi/v/message-flow.svg)](https://pypi.python.org/pypi/message-flow)
[![downloads](https://static.pepy.tech/badge/message-flow/month)](https://pepy.tech/project/message-flow)<br>
[![license](https://img.shields.io/github/license/voro6yov/message-flow.svg)](https://github.com/voro6yov/message-flow/blob/main/LICENSE)

Message Flow is a first Web framework for building event-driven applications with Python 3.10+.

Asynchronous APIs, which allow servers to push notifications and data directly to the client as soon as available, are becoming increasingly important in modern applications that offer instant feedback and streaming data. Message Flow gives you all the tools needed to implement asynchronous APIs.

## Why use Message Flow

- **Fully-featured**: Supports *pub-sub* and *request-async response* communication patterns.
- **Easy**: Designed to be easy to use and learn. Less time reading docs.
- **Reliable**: Production-ready framework, equipped with automated, interactive documentation.
- **Standards-based**: Based on (and fully compatible with) the open standard [AsyncAPI](https://www.asyncapi.com) and [JSON Schema](https://json-schema.org).

## Installation

Installing Message Flow is as simple as:

```console
pip install message-flow
```

## Requirements

Python 3.10+

- [Pydantic](https://docs.pydantic.dev/latest/) for the messages serialization and deserialization.

## Message Flow Examples

To see Message Flow at work, let's start with a simple example, creating a consumer and publisher of OrderCreated event:

- Create a file *publisher.py* with:

```python title="OrderCreated event publishing"
from message_flow import MessageFlow, Message, Payload, Header


class OrderCreated(Message):
    order_id: str = Payload()
    tenant_id: str = Header()


if __name__ == "__main__":
    app = MessageFlow()

    app.publish(OrderCreated(order_id="order_id", tenant_id="tenant_id"), channel_address="orders")
    
```

- Create a file *dispatcher.py* with:

```python title="OrderCreated event dispatching"
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

```

- Run the dispatcher with:

```console
$ python dispatcher.py
```

- Open another terminal and publish message with:

```console
$ python publisher.py
```

- In terminal with running dispatcher you should see the following message:

```console
Event received order_id tenant_id
```