from event_flow.utils import export
from event_flow.messaging import MessageProducer
from event_flow.serde import Serializer

from ..shared import DomainEvent, DomainEventMessageFactory, DomainEventNameMapping
from .domain_event_publisher import DomainEventPublisher


@export
class DomainEventPublisherImpl(DomainEventPublisher):
    def __init__(
        self,
        message_producer: MessageProducer,
        domain_event_name_mapping: DomainEventNameMapping,
        serializer: Serializer,
    ) -> None:
        self._message_producer = message_producer
        self._domain_event_name_mapping = domain_event_name_mapping
        self._serializer = serializer

    def publish(
        self,
        aggregate_type: str,
        aggregate_id: str,
        domain_events: list[DomainEvent],
        *,
        headers: dict[str, str] | None = None,
    ) -> None:
        for domain_event in domain_events:
            self._message_producer.send(
                aggregate_type,
                DomainEventMessageFactory.make(
                    aggregate_type,
                    aggregate_id,
                    self._serializer.serialize(domain_event),
                    self._domain_event_name_mapping.event_to_external_event_type(aggregate_type, domain_event),
                    headers=headers,
                ),
            )
