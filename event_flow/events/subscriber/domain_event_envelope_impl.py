from typing import TypeVar

from event_flow.utils import export
from event_flow.messaging import Message

from ..shared import DomainEvent
from .domain_event_envelope import DomainEventEnvelope

T = TypeVar("T", bound=DomainEvent)


@export
class DomainEventEnvelopeImpl(DomainEventEnvelope[T]):
    def __init__(
        self,
        message: Message,
        aggregate_type: str,
        aggregate_id: str,
        event_id: str,
        event: T,
    ) -> None:
        self._message = message
        self._aggregate_type = aggregate_type
        self._aggregate_id = aggregate_id
        self._event_id = event_id
        self._event = event

    @property
    def aggregate_id(self) -> str:
        return self._aggregate_id

    @property
    def message(self) -> Message:
        return self._message

    @property
    def event(self) -> T:
        return self._event

    @property
    def aggregate_type(self) -> str:
        return self._aggregate_type

    @property
    def event_id(self) -> str:
        return self._event_id
