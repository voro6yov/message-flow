from typing import Callable

from event_flow.utils import export
from event_flow.messaging import Message

from ..shared import DomainEvent, EventMessageHeaders
from .domain_event_envelope import DomainEventEnvelope


@export
class DomainEventHandler:
    def __init__(
        self,
        aggregate_type: str,
        event_class: type[DomainEvent],
        handler: Callable[[DomainEventEnvelope[DomainEvent]], None],
    ) -> None:
        self._aggregate_type = aggregate_type
        self._event_class = event_class
        self._handler = handler

    @property
    def aggregate_type(self) -> str:
        return self._aggregate_type

    @property
    def event_class(self) -> str:
        return self._event_class

    def handles(self, message: Message) -> bool:
        return self._aggregate_type == message.get_required_header(
            EventMessageHeaders.AGGREGATE_TYPE
        ) and self._event_class.__name__ == message.get_required_header(EventMessageHeaders.EVENT_TYPE)

    def invoke(self, domain_event_envelope: DomainEventEnvelope[DomainEvent]) -> None:
        self._handler(domain_event_envelope)
