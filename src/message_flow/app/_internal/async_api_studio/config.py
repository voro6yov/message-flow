from typing import Literal, TypedDict

from ....utils import internal


@internal
class ShowingOptions(TypedDict, total=False):
    sidebar: bool
    info: bool
    servers: bool
    operations: bool
    messages: bool
    schemas: bool
    errors: bool


@internal
class ExpandingOptions(TypedDict, total=False):
    messageExamples: bool


@internal
class SidebarOptions(TypedDict, total=False):
    showServers: Literal["byDefault"]
    showOperations: Literal["byDefault"]


@internal
class AsyncAPIStudioConfig(TypedDict):
    show: ShowingOptions
    expand: ExpandingOptions
    sidebar: SidebarOptions


@internal
class AsyncAPIStudio(TypedDict):
    schema: str
    config: AsyncAPIStudioConfig
