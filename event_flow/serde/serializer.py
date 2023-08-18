from typing import Protocol, TypeVar

from event_flow.utils import export
from event_flow.events import DomainEvent

T = TypeVar("T", contravariant=True, bound=DomainEvent)


@export
class Serializer(Protocol[T]):
    def serialize(self, obj: T) -> str:
        ...
