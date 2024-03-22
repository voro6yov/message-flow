from uuid import uuid4

import pytest
from pydantic import BaseModel

from message_flow import CorrelationId, Header, Message, MessageInfo, MessageTrait, Payload


def test_message__payload_and_headers():
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


def test_message__deserialization():
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

    test_payload = b'{"p1":"p1 value","p2":{"p2":"p2 value"}}'
    test_headers = {"h1": {"h2": "h2 value"}, "message_id": "message_id_value"}

    test_message: Example = Example.from_payload_and_headers(test_payload, test_headers)

    assert isinstance(test_message.p1, str)
    assert isinstance(test_message.p2, P2)
    assert isinstance(test_message.h1, H1)


def test_message__payload_and_headers__with_default_factory():
    class Example(Message):
        p1: str = Payload(default_factory=lambda: uuid4().hex)
        h1: str = Header(default_factory=lambda: uuid4().hex)

    test_message = Example(p1="p1_value")

    assert test_message.payload and test_message.headers
    assert "p1_value" == test_message.p1
    assert test_message.h1 is not None


def test_message__without_payload_and_headers():
    class Example(Message):
        pass

    test_message = Example()

    assert b"{}" == test_message.payload
    assert {} == test_message.headers


def test_message__explicit_constructor():
    with pytest.raises(RuntimeError):

        class Example(Message):
            p1: str = Payload()
            h1: str = Header()

            def __init__(self, *, p1: str, h1: str) -> None:
                self.p1 = p1
                self.h1 = h1
