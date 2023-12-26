from typing import TypedDict

from typing_extensions import Required

from ...utils import internal


@internal
class OperationInfo(TypedDict, total=False):
    channel: Required[str]
    title: str
    summary: str
    description: str
