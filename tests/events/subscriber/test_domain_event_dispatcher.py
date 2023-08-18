from queue import Empty, Queue

from event_flow.events import (
    DomainEventDispatcher,
    DomainEventEnvelope,
    DomainEventMessageFactory,
)
from event_flow.messaging import Message

from .example_domain_event import ExampleDomainEvent


def test_should_dispatch_message(
    dispatcher: DomainEventDispatcher,
    aggregate_type: str,
    aggregate_id: str,
    queue: Queue,
    message_id: str,
):
    dispatcher.initialize()

    dispatcher.message_handler(
        DomainEventMessageFactory.make(
            aggregate_type, aggregate_id, "", ExampleDomainEvent.__name__, headers={Message.ID: message_id}
        )
    )

    try:
        dee: DomainEventEnvelope = queue.get_nowait()
    except Empty:
        dee = None

    assert dee is not None

    assert aggregate_type == dee.aggregate_type
    assert aggregate_id == dee.aggregate_id
    assert message_id == dee.event_id
