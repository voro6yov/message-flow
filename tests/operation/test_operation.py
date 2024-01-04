import pytest

from message_flow import Message
from message_flow.operation import Operation


def test_operation():
    class Empty(Message):
        ...

    test_operation = Operation.as_event(
        message=Empty,
        channel="channel",
        title="Operation title",
        summary="Operation summary",
        description="Operation description",
    )

    with pytest.raises(RuntimeError):
        test_operation(Empty())
