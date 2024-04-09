import inspect
from typing import TYPE_CHECKING, Any, Callable, get_args

from ..utils import internal
from .typed_annotation import TypedAnnotation

if TYPE_CHECKING:
    from types import FrameType


@internal
class Call:
    def __init__(self, call: Callable) -> None:
        self._call = call

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
