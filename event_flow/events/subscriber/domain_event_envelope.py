from typing import Protocol, TypeVar

from event_flow.utils import export
from event_flow.messaging import Message

from ..shared import DomainEvent

T = TypeVar("T", covariant=True, bound=DomainEvent)


@export
class DomainEventEnvelope(Protocol[T]):
    @property
    def aggregate_id(self) -> str:
        ...

    @property
    def message(self) -> Message:
        ...

    @property
    def aggregate_type(self) -> str:
        ...

    @property
    def event_id(self) -> str:
        ...
