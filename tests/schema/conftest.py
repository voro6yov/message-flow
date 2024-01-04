from unittest import mock

import pytest
from pydantic import BaseModel

from message_flow import Channel, CorrelationId, Header, Message, MessageFlow, MessageInfo, MessageTrait, Payload
from message_flow.operation import Operation


@pytest.fixture
def example_message():
    class CorrelationIdTrait(MessageTrait):
        message_id: str = Header()
        correlation_id = CorrelationId("message_id")

    class P2(BaseModel):
        p2: str

    class Example(Message):
        message_info = MessageInfo(
            title="Test Message",
            summary="Test Message Summary",
            description="Test Message Description",
            traits=[CorrelationIdTrait],
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
                "payload": {
                    "properties": {"p1": {"title": "P1", "type": "string"}, "p2": {"$ref": "#/components/schemas/P2"}},
                    "required": ["p1", "p2"],
                    "title": "payload",
                    "type": "object",
                },
                "headers": {
                    "properties": {
                        "h1": {"title": "H1", "type": "string"},
                        "message_id": {"title": "Message Id", "type": "string"},
                    },
                    "required": ["h1", "message_id"],
                    "title": "headers",
                    "type": "object",
                },
                "correlationId": {"location": "$message.header#/message_id"},
                "title": "Test Message",
                "summary": "Test Message Summary",
                "description": "Test Message Description",
            }
        },
    }


@pytest.fixture
def example_operation(example_message):
    return Operation.as_command(
        message=example_message,
        reply=example_message,
        reply_channel="reply-channel",
        channel="channel",
        title="Operation title",
        summary="Operation summary",
        description="Operation description",
    )


@pytest.fixture
def example_operation_components():
    return {
        "schemas": {},
        "channels": {},
        "operations": {
            "sendExample": {
                "action": "send",
                "channel": {"$ref": "#/channels/channel"},
                "messages": [{"$ref": "#/channels/channel/messages/Example"}],
                "title": "Operation title",
                "summary": "Operation summary",
                "description": "Operation description",
                "reply": {
                    "channel": {"$ref": "#/channels/reply-channel"},
                    "messages": [{"$ref": "#/components/messages/Example"}],
                },
            }
        },
        "messages": {},
    }


@pytest.fixture
def reply_channel():
    return Channel(
        "test_reply_address",
        title="Reply Channel title",
        summary="Reply Channel summary",
        description="Reply Channel description",
    )


@pytest.fixture
def event():
    class Event(Message):
        message_info = MessageInfo(
            title="Event",
            summary="Event Summary",
            description="Event Description",
        )
        p1: str = Payload()
        h1: str = Header()

    return Event


@pytest.fixture
def command():
    class Command(Message):
        message_info = MessageInfo(
            title="Command",
            summary="Command Summary",
            description="Command Description",
        )
        p1: str = Payload()
        h1: str = Header()

    return Command


@pytest.fixture
def command_reply():
    class CommandReply(Message):
        message_info = MessageInfo(
            title="CommandReply",
            summary="CommandReply Summary",
            description="CommandReply Description",
        )
        p1: str = Payload()
        h1: str = Header()

    return CommandReply


@pytest.fixture
def example_channel(event, command, command_reply, reply_channel, example_message):
    channel = Channel(
        "test_address",
        title="Channel title",
        summary="Channel summary",
        description="Channel description",
    )

    channel.publish()(event)
    channel.send(reply=command_reply, reply_channel=reply_channel)(command)
    channel.subscribe(example_message)(mock.Mock())

    return channel


@pytest.fixture
def example_channel_components():
    return {
        "schemas": {
            "P2": {
                "properties": {"p2": {"title": "P2", "type": "string"}},
                "required": ["p2"],
                "title": "P2",
                "type": "object",
            }
        },
        "channels": {
            "test_address": {
                "address": "test_address",
                "messages": {
                    "Event": {"$ref": "#/components/messages/Event"},
                    "Command": {"$ref": "#/components/messages/Command"},
                    "Example": {"$ref": "#/components/messages/Example"},
                },
                "title": "Channel title",
                "summary": "Channel summary",
                "description": "Channel description",
            }
        },
        "operations": {
            "sendEvent": {
                "action": "send",
                "channel": {"$ref": "#/channels/test_address"},
                "messages": [{"$ref": "#/channels/test_address/messages/Event"}],
            },
            "sendCommand": {
                "action": "send",
                "channel": {"$ref": "#/channels/test_address"},
                "messages": [{"$ref": "#/channels/test_address/messages/Command"}],
                "reply": {
                    "channel": {"$ref": "#/channels/test_reply_address"},
                    "messages": [{"$ref": "#/components/messages/CommandReply"}],
                },
            },
            "receiveExample": {
                "action": "receive",
                "channel": {"$ref": "#/channels/test_address"},
                "messages": [{"$ref": "#/channels/test_address/messages/Example"}],
            },
        },
        "messages": {
            "Event": {
                "contentType": "application/json",
                "payload": {
                    "properties": {"p1": {"title": "P1", "type": "string"}},
                    "required": ["p1"],
                    "title": "payload",
                    "type": "object",
                },
                "headers": {
                    "properties": {"h1": {"title": "H1", "type": "string"}},
                    "required": ["h1"],
                    "title": "headers",
                    "type": "object",
                },
                "title": "Event",
                "summary": "Event Summary",
                "description": "Event Description",
            },
            "Command": {
                "contentType": "application/json",
                "payload": {
                    "properties": {"p1": {"title": "P1", "type": "string"}},
                    "required": ["p1"],
                    "title": "payload",
                    "type": "object",
                },
                "headers": {
                    "properties": {"h1": {"title": "H1", "type": "string"}},
                    "required": ["h1"],
                    "title": "headers",
                    "type": "object",
                },
                "title": "Command",
                "summary": "Command Summary",
                "description": "Command Description",
            },
            "Example": {
                "contentType": "application/json",
                "payload": {
                    "properties": {"p1": {"title": "P1", "type": "string"}, "p2": {"$ref": "#/components/schemas/P2"}},
                    "required": ["p1", "p2"],
                    "title": "payload",
                    "type": "object",
                },
                "headers": {
                    "properties": {
                        "h1": {"title": "H1", "type": "string"},
                        "message_id": {"title": "Message Id", "type": "string"},
                    },
                    "required": ["h1", "message_id"],
                    "title": "headers",
                    "type": "object",
                },
                "correlationId": {"location": "$message.header#/message_id"},
                "title": "Test Message",
                "summary": "Test Message Summary",
                "description": "Test Message Description",
            },
        },
    }


@pytest.fixture
def example_message_flow(example_channel):
    return MessageFlow(channels=[example_channel])


@pytest.fixture
def example_message_flow_components():
    return {
        "asyncapi": "3.0.0",
        "info": {"title": "MessageFlow", "version": "0.1.0"},
        "channels": {"test_address": {"$ref": "#/components/channels/test_address"}},
        "operations": {
            "sendEvent": {"$ref": "#/components/operations/sendEvent"},
            "sendCommand": {"$ref": "#/components/operations/sendCommand"},
            "receiveExample": {"$ref": "#/components/operations/receiveExample"},
        },
        "components": {
            "schemas": {
                "P2": {
                    "properties": {"p2": {"title": "P2", "type": "string"}},
                    "required": ["p2"],
                    "title": "P2",
                    "type": "object",
                }
            },
            "channels": {
                "test_address": {
                    "address": "test_address",
                    "messages": {
                        "Event": {"$ref": "#/components/messages/Event"},
                        "Command": {"$ref": "#/components/messages/Command"},
                        "Example": {"$ref": "#/components/messages/Example"},
                    },
                    "title": "Channel title",
                    "summary": "Channel summary",
                    "description": "Channel description",
                }
            },
            "operations": {
                "sendEvent": {
                    "action": "send",
                    "channel": {"$ref": "#/channels/test_address"},
                    "messages": [{"$ref": "#/channels/test_address/messages/Event"}],
                },
                "sendCommand": {
                    "action": "send",
                    "channel": {"$ref": "#/channels/test_address"},
                    "messages": [{"$ref": "#/channels/test_address/messages/Command"}],
                    "reply": {
                        "channel": {"$ref": "#/channels/test_reply_address"},
                        "messages": [{"$ref": "#/components/messages/CommandReply"}],
                    },
                },
                "receiveExample": {
                    "action": "receive",
                    "channel": {"$ref": "#/channels/test_address"},
                    "messages": [{"$ref": "#/channels/test_address/messages/Example"}],
                },
            },
            "messages": {
                "Event": {
                    "contentType": "application/json",
                    "payload": {
                        "properties": {"p1": {"title": "P1", "type": "string"}},
                        "required": ["p1"],
                        "title": "payload",
                        "type": "object",
                    },
                    "headers": {
                        "properties": {"h1": {"title": "H1", "type": "string"}},
                        "required": ["h1"],
                        "title": "headers",
                        "type": "object",
                    },
                    "title": "Event",
                    "summary": "Event Summary",
                    "description": "Event Description",
                },
                "Command": {
                    "contentType": "application/json",
                    "payload": {
                        "properties": {"p1": {"title": "P1", "type": "string"}},
                        "required": ["p1"],
                        "title": "payload",
                        "type": "object",
                    },
                    "headers": {
                        "properties": {"h1": {"title": "H1", "type": "string"}},
                        "required": ["h1"],
                        "title": "headers",
                        "type": "object",
                    },
                    "title": "Command",
                    "summary": "Command Summary",
                    "description": "Command Description",
                },
                "Example": {
                    "contentType": "application/json",
                    "payload": {
                        "properties": {
                            "p1": {"title": "P1", "type": "string"},
                            "p2": {"$ref": "#/components/schemas/P2"},
                        },
                        "required": ["p1", "p2"],
                        "title": "payload",
                        "type": "object",
                    },
                    "headers": {
                        "properties": {
                            "h1": {"title": "H1", "type": "string"},
                            "message_id": {"title": "Message Id", "type": "string"},
                        },
                        "required": ["h1", "message_id"],
                        "title": "headers",
                        "type": "object",
                    },
                    "correlationId": {"location": "$message.header#/message_id"},
                    "title": "Test Message",
                    "summary": "Test Message Summary",
                    "description": "Test Message Description",
                },
            },
        },
    }
