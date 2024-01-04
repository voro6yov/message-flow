from uuid import uuid4

import pytest

from message_flow import Header, Message, Payload


@pytest.fixture
def test_channel():
    return uuid4().hex


@pytest.fixture
def another_test_channel():
    return uuid4().hex


@pytest.fixture
def test_message():
    class TestMessage(Message):
        value: str = Payload()
        correlation_id: str = Header()

    return TestMessage


@pytest.fixture
def another_test_message():
    class AnotherTestMessage(Message):
        value: str = Payload()
        correlation_id: str = Header()

    return AnotherTestMessage


@pytest.fixture
def test_message_object(test_message):
    return test_message(value=uuid4().hex, correlation_id=uuid4().hex)


@pytest.fixture
def another_test_message_object(another_test_message):
    return another_test_message(value=uuid4().hex, correlation_id=uuid4().hex)
