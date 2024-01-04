from uuid import uuid4

from message_flow import CorrelationId, Header, Message, MessageInfo, MessageTrait, Payload


def test_traits__basic_attributes_included():
    class Trait(MessageTrait):
        title = "Test Message"
        summary = "Test Message Summary"
        description = "Test Message Description"

    class Example(Message):
        message_info = MessageInfo(
            traits=[Trait],
        )
        p1: str = Payload()
        h1: str = Header()

    assert Trait.title == Example.message_info["title"]
    assert Trait.summary == Example.message_info["summary"]
    assert Trait.description == Example.message_info["description"]


def test_traits__title_is_not_merged():
    class Trait(MessageTrait):
        title = "Test Message Trait"
        summary = "Test Message Summary"
        description = "Test Message Description"

    class Example(Message):
        message_info = MessageInfo(
            title="Test Message",
            traits=[Trait],
        )
        p1: str = Payload()
        h1: str = Header()

    assert Trait.title != Example.message_info["title"]
    assert Trait.summary == Example.message_info["summary"]
    assert Trait.description == Example.message_info["description"]


def test_traits__header_included():
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
        h1: str = Header("h1 value")

    assert "message_id" in Example.headers_attributes()
    assert "correlation_id" in Example.message_info


def test_traits__header_not_included():
    class CorrelationIdTrait(MessageTrait):
        message_id: int = Header()
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
        message_id: str = Header(default_factory=lambda: uuid4().hex)

    assert Example.__dict__["message_id"] != CorrelationIdTrait.__dict__["message_id"]
    assert Example.__annotations__["message_id"] is str


def test_traits__several_traits():
    class Trait(MessageTrait):
        title = "Test Message Trait"
        summary = "Test Message Summary Trait"
        description = "Test Message Description Trait"

    class CorrelationIdTrait(MessageTrait):
        message_id: int = Header()
        correlation_id = CorrelationId("message_id", "Used to trace messages")
        description = "Test Message Description Correlation Id Trait"

    class Example(Message):
        message_info = MessageInfo(
            title="Test Message",
            traits=[CorrelationIdTrait, Trait],
        )
        p1: str = Payload()
        h1: str = Header()
        message_id: str = Header(default_factory=lambda: uuid4().hex)

    assert Trait.title != Example.message_info["title"]
    assert Trait.summary == Example.message_info["summary"]
    assert CorrelationIdTrait.description == Example.message_info["description"]

    assert Example.__dict__["message_id"] != CorrelationIdTrait.__dict__["message_id"]
    assert Example.__annotations__["message_id"] is str
