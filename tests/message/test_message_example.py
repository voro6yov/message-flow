from pydantic import BaseModel

from message_flow import CorrelationId, Header, Message, MessageInfo, MessageTrait, Payload


def test_message_example():
    class CorrelationIdTrait(MessageTrait):
        message_id: str = Header()
        correlation_id = CorrelationId("message_id")

    class P2(BaseModel):
        p2: str

    class H1(BaseModel):
        h2: str

    class Example(Message):
        message_info = MessageInfo(
            title="Test Message",
            summary="Test Message Summary",
            description="Test Message Description",
            traits=[CorrelationIdTrait],
        )
        p1: str = Payload()
        p2: P2 = Payload()
        h1: H1 = Header(H1(h2="h2 value"))

    test_message = Example(p1="p1 value", p2=P2(p2="p2 value"), message_id="message_id_value")

    assert test_message.payload and test_message.headers
    assert b'{"p1":"p1 value","p2":{"p2":"p2 value"}}' == test_message.payload
    assert {"h1": {"h2": "h2 value"}, "message_id": "message_id_value"} == test_message.headers
