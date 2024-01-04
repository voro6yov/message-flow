from typing import Any

from message_flow import Channel


def test_channel_schema(example_channel: Channel, example_channel_components: dict[str, Any]):
    assert example_channel_components == example_channel.__async_api_components__.as_schema()
