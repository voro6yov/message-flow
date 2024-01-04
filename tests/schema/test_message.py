from typing import Any

from message_flow import Message


def test_message_schema(example_message: Message, example_message_components: dict[str, Any]):
    assert example_message_components == example_message.__async_api_components__.as_schema()
