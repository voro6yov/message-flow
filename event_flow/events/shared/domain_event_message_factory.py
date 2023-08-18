from uuid import uuid4

from event_flow.utils import export
from event_flow.messaging import Message, MessageBuilder

from .event_message_headers import EventMessageHeaders


@export
class DomainEventMessageFactory:
    @staticmethod
    def make(
        aggregate_type: str,
        aggregate_id: str,
        payload: str,
        event_type: str,
        *,
        headers: dict[str, str] | None = None,
    ) -> Message:
        return (
            MessageBuilder.with_payload(payload)
            .with_header(EventMessageHeaders.AGGREGATE_ID, aggregate_id)
            .with_header(EventMessageHeaders.AGGREGATE_TYPE, aggregate_type)
            .with_header(EventMessageHeaders.EVENT_TYPE, event_type)
            .with_header(Message.ID, uuid4().hex)
            .with_extra_headers("", headers if headers else {})
            .build()
        )
