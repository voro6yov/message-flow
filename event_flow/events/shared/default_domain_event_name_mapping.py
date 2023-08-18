from event_flow.utils import export
from event_flow.events.shared.domain_event import DomainEvent

from .domain_event_name_mapping import DomainEventNameMapping


@export
class DefaultDomainEventNameMapping(DomainEventNameMapping):
    def event_to_external_event_type(self, aggregate_type: str, event: DomainEvent) -> str:
        return event.__class__.__name__

    def external_event_type_to_event_class_name(self, aggregate_type: str, event_type_header: str) -> str:
        return event_type_header
