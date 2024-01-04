import json
from typing import Any

from message_flow import MessageFlow


def test_message_schema(example_message_flow: MessageFlow, example_message_flow_components: dict[str, Any]):
    assert json.dumps(example_message_flow_components) == example_message_flow.make_async_api_schema()
