from event_flow.utils import export


@export
class EventMessageHeaders:
    EVENT_TYPE: str = "event-type"
    AGGREGATE_TYPE: str = "event-aggregate-type"
    AGGREGATE_ID: str = "event-aggregate-id"
