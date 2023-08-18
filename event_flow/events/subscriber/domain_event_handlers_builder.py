from typing import Callable, Type

from event_flow.utils import export

from ..shared import DomainEvent
from .domain_event_envelope import DomainEventEnvelope, T
from .domain_event_handler import DomainEventHandler
from .domain_event_handlers import DomainEventHandlers


@export
class DomainEventHandlersBuilder:
    def __init__(self, aggregate_type: str) -> None:
        self._aggregate_type = aggregate_type
        self._handlers: list[DomainEventHandler] = []

    @classmethod
    def for_aggregate_type(cls, aggregate_type: str) -> "DomainEventHandlersBuilder":
        return cls(aggregate_type)

    def on_event(
        self,
        event_class: Type[T],
        handler: Callable[[DomainEventEnvelope[DomainEvent]], None],
    ) -> "DomainEventHandlersBuilder":
        self._handlers.append(DomainEventHandler(self._aggregate_type, event_class, handler))
        return self

    def and_for_aggregate_type(self, aggregate_type: str) -> "DomainEventHandlersBuilder":
        self._aggregate_type = aggregate_type
        return self

    def build(self) -> DomainEventHandlers:
        return DomainEventHandlers(self._handlers)
