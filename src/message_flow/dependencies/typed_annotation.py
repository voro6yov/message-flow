from typing import Annotated, Any, ForwardRef, get_args, get_origin

from pydantic._internal._typing_extra import (  # type: ignore[no-redef]
    eval_type_lenient,
)

from ..utils import internal


@internal
class TypedAnnotation:
    def __init__(self, annotation: Any, globals: dict[str, Any], locals: dict[str, Any]) -> None:
        self._raw_annotation = annotation
        self._globals = globals
        self._locals = locals

    def __call__(self) -> Any:
        annotation = self._raw_annotation

        if isinstance(annotation, str):
            annotation = ForwardRef(annotation)

        if isinstance(annotation, ForwardRef):
            annotation = eval_type_lenient(annotation, self._globals, self._locals)

        if get_origin(annotation) is Annotated and (args := get_args(annotation)):
            solved_args = [self.from_current_annotation(arg)() for arg in args]
            annotation.__origin__, annotation.__metadata__ = solved_args[0], solved_args[1:]

        return annotation

    def from_current_annotation(self, annotation: Any) -> "TypedAnnotation":
        return TypedAnnotation(annotation=annotation, globals=self._globals, locals=self._locals)
