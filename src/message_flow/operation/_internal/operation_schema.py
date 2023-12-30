from typing import TypedDict

from ...utils import internal


@internal
class OperationReplySchema(TypedDict, total=False):
    channel: dict[str, str]
    messages: list[dict[str, str]]


@internal
class OperationSchema(TypedDict, total=False):
    action: str
    channel: dict[str, str]
    title: str
    summary: str
    description: str
    messages: list[dict[str, str]]
    reply: OperationReplySchema
