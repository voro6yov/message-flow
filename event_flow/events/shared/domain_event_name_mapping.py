from typing import Protocol

from event_flow.utils import export

from .domain_event import DomainEvent


@export
class DomainEventNameMapping(Protocol):
    def event_to_external_event_type(self, aggregate_type: str, event: DomainEvent) -> str:
        ...

    def external_event_type_to_event_class_name(self, aggregate_type: str, event_type_header: str) -> str:
        ...
