from typing import TypedDict

from ...utils import internal


@internal
class ChannelInfo(TypedDict, total=False):
    title: str
    summary: str
    description: str
