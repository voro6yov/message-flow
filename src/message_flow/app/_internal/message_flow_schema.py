from typing import Any, TypedDict

from ...utils import internal


@internal
class Info(TypedDict):
    title: str
    version: str


@internal
class MessageFlowSchema(TypedDict):
    asyncapi: str
    info: Info
    channels: dict[str, dict[str, Any]]
    operations: dict[str, dict[str, Any]]
    components: dict[str, dict[str, Any]]
