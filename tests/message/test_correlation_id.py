import pytest

from message_flow import CorrelationId, Header, Message, MessageInfo, MessageTrait, Payload


def test__correlation_header_is_not_set():
    class CorrelationIdTrait(MessageTrait):
        correlation_id = CorrelationId("message_id")

    with pytest.raises(RuntimeError):

        class Example(Message):
            message_info = MessageInfo(
                title="Test Message",
                summary="Test Message Summary",
                description="Test Message Description",
                traits=[CorrelationIdTrait],
            )
            p1: str = Payload()
            h1: str = Header()


def test__correlation_id_added():
    class CorrelationIdTrait(MessageTrait):
        message_id: str = Header()
        correlation_id = CorrelationId("message_id")

    class Example(Message):
        message_info = MessageInfo(
            title="Test Message",
            summary="Test Message Summary",
            description="Test Message Description",
            traits=[CorrelationIdTrait],
        )
        p1: str = Payload()
        h1: str = Header()

    assert set(CorrelationIdTrait.headers_attributes()).issubset(set(Example.headers_attributes()))
