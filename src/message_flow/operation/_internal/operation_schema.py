from typing import TypedDict

from ...utils import internal


@internal
class OperationSchema(TypedDict, total=False):
    action: str
    channel: dict[str, str]
    title: str
    summary: str
    description: str
    messages: list[dict[str, str]]
