from typing import Any

from message_flow.operation import Operation


def test_operation_schema(example_operation: Operation, example_operation_components: dict[str, Any]):
    assert example_operation_components == example_operation.__async_api_components__.as_schema()
