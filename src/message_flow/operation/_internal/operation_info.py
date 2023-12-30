from typing import TypedDict

from typing_extensions import Required

from ...utils import internal
from ...message import Message


@internal
class OperationReply(TypedDict):
    channel: str
    messages: list[type[Message]]


@internal
class OperationInfo(TypedDict, total=False):
    channel: Required[str]
    title: str
    summary: str
    description: str
    reply: OperationReply
