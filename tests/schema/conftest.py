import pytest
from pydantic import BaseModel

from event_flow import Header, Message, MessageInfo, Payload


@pytest.fixture
def example_message():
    class P2(BaseModel):
        p2: str

    class Example(Message):
        message_info = MessageInfo(
            title="Test Message",
            summary="Test Message Summary",
            description="Test Message Description",
        )
        p1: str = Payload()
        p2: P2 = Payload()
        h1: str = Header()

    return Example


@pytest.fixture
def example_message_components():
    return {
        "schemas": {
            "P2": {
                "properties": {"p2": {"title": "P2", "type": "string"}},
                "required": ["p2"],
                "title": "P2",
                "type": "object",
            }
        },
        "channels": {},
        "operations": {},
        "messages": {
            "Example": {
                "contentType": "application/json",
                "headers": {
                    "properties": {"h1": {"title": "H1", "type": "string"}},
                    "required": ["h1"],
                    "title": "headers",
                    "type": "object",
                },
                "payload": {
                    "properties": {
                        "p1": {"title": "P1", "type": "string"},
                        "p2": {"$ref": "#/components/schemas/P2"},
                    },
                    "required": ["p1", "p2"],
                    "title": "payload",
                    "type": "object",
                },
                "title": "Test Message",
                "summary": "Test Message Summary",
                "description": "Test Message Description",
            }
        },
    }
