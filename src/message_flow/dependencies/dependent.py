from typing import Any, Callable

from pydantic import BaseModel

from ..utils import internal


@internal
class Dependent:
    def __init__(
        self,
        call: Callable,
        model: BaseModel | None = None,
        response_model: BaseModel | None = None,
        class_fields: None = None,
        dependencies: None = None,
        positional_args: None = None,
        keyword_args: None = None,
    ) -> None:
        self.call = call
        self.model = model
        self.response_model = response_model
        self.class_fields: dict[str, tuple[Any, Any]] = class_fields
        self.dependencies: dict[str, "Dependent"] = dependencies
        self.positional_args: list[str] = positional_args
        self.keyword_args: list[str] = keyword_args

    @classmethod
    def for_call(cls, *, call: Callable) -> "Dependent":
        return Dependent(call=call)
