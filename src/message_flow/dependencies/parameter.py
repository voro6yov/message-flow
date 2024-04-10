from typing import Annotated, Any, Callable, get_args, get_origin
import inspect
from ..utils import internal
from .typed_annotation import TypedAnnotation
from .depends import Depends


@internal
class Parameter:
    def __init__(
        self,
        name: str,
        kind: inspect._ParameterKind,
        default: Any,
        typed_annotation: TypedAnnotation,
    ) -> None:
        self.name = name
        self.kind = kind
        self.default = default
        self.typed_annotation = typed_annotation()

        self.dep = None

    @property
    def annotation(self) -> Any:
        if not hasattr(self, "_annotation"):
            if self.annotation is inspect.Parameter.empty:
                annotation = Any
            elif get_origin(self.annotation) is Annotated:
                annotated_args = get_args(self.annotation)
                type_annotation = annotated_args[0]
                custom_annotations = [
                    arg for arg in annotated_args[1:] if isinstance(arg, Depends)
                ]

                assert (
                    len(custom_annotations) <= 1
                ), f"Cannot specify multiple `Annotated` Custom arguments for `{self.name}`!"

                next_custom = next(iter(custom_annotations), None)
                if next_custom is not None:
                    if isinstance(next_custom, Depends):
                        self.dep = next_custom
                    else:  # pragma: no cover
                        raise AssertionError("unreachable")

                    annotation = type_annotation
                else:
                    annotation = self.annotation
            else:
                annotation = self.annotation
            
            self._annotation = annotation
        
        return self._annotation
    
    @property
    def default(self) -> Any:
        if not hasattr(self, "_default"):
            if self.name == "args":
                default = ()
            elif self.name == "kwargs":
                default = {}
            else:
                default = self.default
            
            self._default = default
        
        return self._default
