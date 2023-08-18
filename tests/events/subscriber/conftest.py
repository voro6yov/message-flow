from queue import Queue
from unittest import mock
from uuid import uuid4

import pytest

from event_flow.events import (
    DomainEventDispatcher,
    DomainEventEnvelope,
    DomainEventHandlersBuilder,
    DomainEventNameMapping,
)
from event_flow.messaging import MessageConsumer
from event_flow.serde import Deserializer

from .example_domain_event import ExampleDomainEvent


@pytest.fixture
def event_dispatcher_id():
    return uuid4().hex


@pytest.fixture
def aggregate_type():
    return uuid4().hex


@pytest.fixture
def aggregate_id():
    return uuid4().hex


@pytest.fixture
def message_id():
    return uuid4().hex


@pytest.fixture
def external_event_type():
    return uuid4().hex


@pytest.fixture
def queue() -> Queue:
    return Queue()


@pytest.fixture
def domain_event_handlers(aggregate_type: str, queue: Queue):
    def handle_example_domain_event(event: DomainEventEnvelope[ExampleDomainEvent]) -> None:
        queue.put(event)

    return (
        DomainEventHandlersBuilder.for_aggregate_type(aggregate_type)
        .on_event(ExampleDomainEvent, handle_example_domain_event)
        .build()
    )


@pytest.fixture
def dispatcher(event_dispatcher_id, domain_event_handlers):
    message_consumer: MessageConsumer = mock.create_autospec(MessageConsumer)
    domain_event_name_mapping: DomainEventNameMapping = mock.create_autospec(DomainEventNameMapping)
    deserializer = mock.create_autospec(Deserializer)

    domain_event_name_mapping.external_event_type_to_event_class_name.return_value = ExampleDomainEvent.__name__

    return DomainEventDispatcher(
        event_dispatcher_id,
        domain_event_handlers,
        message_consumer,
        domain_event_name_mapping,
        deserializer,
    )
