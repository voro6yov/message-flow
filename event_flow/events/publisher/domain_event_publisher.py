from typing import Protocol

from event_flow.utils import export

from ..shared import DomainEvent


@export
class DomainEventPublisher(Protocol):
    def publish(
        self,
        aggregate_type: str,
        aggregate_id: str,
        domain_events: list[DomainEvent],
        *,
        headers: dict[str, str] | None = None,
    ) -> None:
        ...
