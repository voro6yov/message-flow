from event_flow.utils import export
from event_flow.messaging import Message

from .domain_event_handler import DomainEventHandler


@export
class DomainEventHandlers:
    def __init__(self, handlers: list[DomainEventHandler]) -> None:
        self._handlers = handlers

    @property
    def handlers(self) -> list[DomainEventHandler]:
        return self._handlers

    @property
    def aggregate_types_and_events(self) -> set[str]:
        return set(map(lambda h: h.aggregate_type, self._handlers))

    def find_target_method(self, message: Message) -> DomainEventHandler | None:
        return next(filter(lambda h: h.handles(message), self._handlers), None)
