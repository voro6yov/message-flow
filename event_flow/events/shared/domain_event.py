from typing import Protocol

from event_flow.utils import export


@export
class DomainEvent(Protocol):
    ...
