# type: ignore
from typing import Annotated, Any, Callable, Literal, final

from pydantic import TypeAdapter
from pydantic.fields import FieldInfo
from pydantic_core import PydanticUndefined as Undefined

from ..utils import external


@final
@external
class Payload(FieldInfo):
    def __init__(
        self,
        default: Any = Undefined,
        *,
        annotation: type[Any] | None = None,
        default_factory: Callable[[], Any] | None = None,
        alias: str | None = None,
        alias_priority: int | None = None,
        validation_alias: str | None = None,
        serialization_alias: str | None = None,
        title: str | None = None,
        description: str | None = None,
        examples: list[Any] | None = None,
        gt: float | None = None,
        ge: float | None = None,
        lt: float | None = None,
        le: float | None = None,
        multiple_of: float | None = Undefined,
        strict: bool | None = Undefined,
        min_length: int | None = None,
        max_length: int | None = None,
        pattern: str | None = None,
        allow_inf_nan: bool | None = Undefined,
        max_digits: int | None = Undefined,
        decimal_places: int | None = Undefined,
        union_mode: Literal["smart", "left_to_right"] | None = None,
        discriminator: str | None = None,
        json_schema_extra: dict[str, Any] | Callable[[dict[str, Any]], None] | None = None,
        **extra: Any,
    ):
        kwargs = dict(
            default=default,
            annotation=annotation,
            default_factory=default_factory,
            alias=alias,
            alias_priority=alias_priority,
            validation_alias=validation_alias,
            serialization_alias=serialization_alias,
            title=title,
            description=description,
            examples=examples,
            gt=gt,
            ge=ge,
            lt=lt,
            le=le,
            multiple_of=multiple_of,
            strict=strict,
            min_length=min_length,
            max_length=max_length,
            pattern=pattern,
            allow_inf_nan=allow_inf_nan,
            max_digits=max_digits,
            decimal_places=decimal_places,
            union_mode=union_mode,
            discriminator=discriminator,
            json_schema_extra=json_schema_extra,
            **extra,
        )
        use_kwargs = {k: v for k, v in kwargs.items() if v is not Undefined}

        super().__init__(**use_kwargs)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.default})"

    def __set_name__(self, owner: Any, name: str) -> None:
        self._private_name = f"_{name}"

    def __get__(self, obj: Any, objtype: Any | None = None) -> Any:
        return getattr(obj, self._private_name)

    def __set__(self, obj: Any, value: Any) -> None:
        self._validate(value)
        setattr(obj, self._private_name, value)

    def _validate(self, value) -> None:
        TypeAdapter(Annotated[self.annotation, self]).validate_python(value)
