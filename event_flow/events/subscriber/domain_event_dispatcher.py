import logging

from event_flow.utils import export
from event_flow.messaging import Message, MessageConsumer
from event_flow.serde import Deserializer

from ..shared import DomainEventNameMapping, EventMessageHeaders
from .domain_event_envelope_impl import DomainEventEnvelopeImpl
from .domain_event_handlers import DomainEventHandlers


@export
class DomainEventDispatcher:
    def __init__(
        self,
        event_dispatcher_id: str,
        domain_event_handlers: DomainEventHandlers,
        message_consumer: MessageConsumer,
        domain_event_name_mapping: DomainEventNameMapping,
        deserializer: Deserializer,
    ) -> None:
        self._event_dispatcher_id = event_dispatcher_id
        self._domain_event_handlers = domain_event_handlers
        self._message_consumer = message_consumer
        self._domain_event_name_mapping = domain_event_name_mapping
        self._deserializer = deserializer

        self._logger = logging.getLogger(self.__class__.__name__)

    def initialize(self) -> None:
        self._logger.info("Initializing domain event dispatcher")
        self._message_consumer.subscribe(
            self._event_dispatcher_id,
            self._domain_event_handlers.aggregate_types_and_events,
            self.message_handler,
        )
        self._logger.info("Initialized domain event dispatcher")

    def message_handler(self, message: Message) -> None:
        aggregate_type = message.get_required_header(EventMessageHeaders.AGGREGATE_TYPE)

        message.set_header(
            EventMessageHeaders.EVENT_TYPE,
            self._domain_event_name_mapping.external_event_type_to_event_class_name(
                aggregate_type,
                message.get_required_header(EventMessageHeaders.EVENT_TYPE),
            ),
        )

        if (handler := self._domain_event_handlers.find_target_method(message)) is None:
            return

        handler.invoke(
            DomainEventEnvelopeImpl(
                message,
                aggregate_type,
                message.get_required_header(EventMessageHeaders.AGGREGATE_ID),
                message.get_required_header(Message.ID),
                self._deserializer.deserialize(handler.event_class, message.payload),
            )
        )
