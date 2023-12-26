from typing import Any, TypedDict

from ...utils import internal


@internal
class MessageSchema(TypedDict, total=False):
    headers: dict[str, Any]
    payload: dict[str, Any]
    correlationId: dict[str, str]
    contentType: str
    title: str
    summary: str
    description: str
