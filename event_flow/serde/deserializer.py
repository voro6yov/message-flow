from typing import Protocol, Type, TypeVar

from event_flow.utils import export
from event_flow.events import DomainEvent

T = TypeVar("T", bound=DomainEvent)


@export
class Deserializer(Protocol[T]):
    def deserialize(self, obj_class: Type[T], payload: str) -> T:
        ...
