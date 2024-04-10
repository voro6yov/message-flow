import inspect
from typing import TYPE_CHECKING, Annotated, Any, Callable, get_args, get_origin

from pydantic import BaseModel, create_model

from ..utils import internal
from .depends import Depends
from .typed_annotation import TypedAnnotation

if TYPE_CHECKING:
    from types import FrameType

from .dependent import Dependent


@internal
class Call:
    def __init__(self, call: Callable) -> None:
        self._call = call

        self.class_fields: dict[str, tuple[Any, Any]] = {}
        self.dependencies: dict[str, "Dependent"] = {}
        self.positional_args: list[str] = []
        self.keyword_args: list[str] = []

    @property
    def name(self) -> str:
        if not hasattr(self, "_name"):
            self._name = getattr(self._call, "__name__", type(self._call).__name__)

        return self._name

    @property
    def signature(self) -> inspect.Signature:
        if not hasattr(self, "_signature"):
            self._signature = inspect.signature(self._call)

        return self._signature

    @property
    def locals(self) -> dict[str, Any]:
        if not hasattr(self, "_locals"):
            frame = inspect.currentframe()

            frames: list["FrameType"] = []

            while frame is not None:
                if "message_flow" not in frame.f_code.co_filename:
                    frames.append(frame)
                frame = frame.f_back

            locals = {}
            for f in frames[::-1]:
                locals.update(f.f_locals)

            self._locals = locals

        return self._locals

    @property
    def globals(self) -> dict[str, Any]:
        if not hasattr(self, "_globals"):
            self._globals = getattr(self._call, "__globals__", {})

        return self._globals

    @property
    def is_gen_callable(self) -> bool:
        if inspect.isgeneratorfunction(self._call):
            return True

        return inspect.isgeneratorfunction(getattr(self._call, "__call__"))

    @property
    def typed_parameters(self) -> inspect.Signature:
        if not hasattr(self, "_typed_parameters"):
            self._typed_parameters = inspect.Signature(
                parameters=[
                    inspect.Parameter(
                        name=parameter.name,
                        kind=parameter.kind,
                        default=parameter.default,
                        annotation=TypedAnnotation(parameter.annotation, self.globals, self.locals)(),
                    )
                    for parameter in self.signature.parameters.values()
                ]
            )

        return self._typed_parameters

    @property
    def return_annotation(self) -> Any:
        if not hasattr(self, "_return_annotation"):
            typed_annotation = TypedAnnotation(self.signature.return_annotation, self.globals, self.locals)()

            if self.is_gen_callable and (return_arguments := get_args(typed_annotation)):
                self._return_annotation = return_arguments[0]
            else:
                self._return_annotation = typed_annotation

        return self._return_annotation
    
    def parse(self, cast: bool = True) -> None:
        for param_name, param in self.typed_parameters.parameters.items():
            dep: Depends | None = None

            if param.annotation is inspect.Parameter.empty:
                annotation = Any
            elif get_origin(param.annotation) is Annotated:
                annotated_args = get_args(param.annotation)
                type_annotation = annotated_args[0]
                custom_annotations = [
                    arg for arg in annotated_args[1:] if isinstance(arg, Depends)
                ]

                assert (
                    len(custom_annotations) <= 1
                ), f"Cannot specify multiple `Annotated` Custom arguments for `{param_name}`!"

                next_custom = next(iter(custom_annotations), None)
                if next_custom is not None:
                    if isinstance(next_custom, Depends):
                        dep = next_custom
                    else:  # pragma: no cover
                        raise AssertionError("unreachable")

                    annotation = type_annotation
                else:
                    annotation = param.annotation
            else:
                annotation = param.annotation

            default: Any
            if param_name == "args":
                default = ()
            elif param_name == "kwargs":
                default = {}
            else:
                default = param.default

            if isinstance(default, Depends):
                assert (
                    not dep
                ), "You can not use `Depends` with `Annotated` and default both"
                dep = default

            elif default is inspect.Parameter.empty:
                self.class_fields[param_name] = (annotation, ...)

            else:
                self.class_fields[param_name] = (annotation, default)

            if dep:
                if not cast:
                    dep.cast = False

                self.dependencies[param_name] = Call(
                    dep.dependency,
                ).parse(cast=dep.cast,)

                if dep.cast is True:
                    self.class_fields[param_name] = (annotation, ...)
                self.keyword_args.append(param_name)

            else:
                if param.kind is param.KEYWORD_ONLY:
                    self.keyword_args.append(param_name)
                elif param_name not in ("args", "kwargs"):
                    self.positional_args.append(param_name)

        call_model = create_model(  # type: ignore[call-overload]
            self.name,
            **self.class_fields,
        )

        response_model: type[BaseModel] | None = None
        if cast and self.return_annotation and self.return_annotation is not inspect.Parameter.empty:
            response_model = create_model(
                "ResponseModel",
                response=(self.return_annotation, ...),
            )

        return Dependent(self._call, call_model, response_model, self.class_fields, self.dependencies, self.positional_args, self.keyword_args)