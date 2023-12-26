from typing import TypedDict

from ...utils import internal


@internal
class ChannelSchema(TypedDict, total=False):
    address: str
    messages: dict[str, dict[str, str]]
    title: str
    summary: str
    description: str
