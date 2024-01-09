# type: ignore
from typing import Annotated, Any, Callable, Literal, final

from pydantic import TypeAdapter
from pydantic.fields import FieldInfo
from pydantic_core import PydanticUndefined as Undefined
from typing_extensions import Doc

from ..utils import external


@final
@external
class Header(FieldInfo):
    """
    Declare a header attribute of the `Message`.

    **Example**

    ```python
    from message_flow import Message, Header

    class CreateOrder(Message):
        correlation_id: str = Header()
    ```
    """

    def __init__(
        self,
        default: Annotated[
            Any,
            Doc(
                """
                Default value if the parameter field is not set.
                """
            ),
        ] = Undefined,
        *,
        default_factory: Annotated[
            Callable[[], Any] | None,
            Doc(
                """
                A callable to generate the default value.
                """
            ),
        ] = None,
        alias: Annotated[
            str | None,
            Doc(
                """
                An alternative name for the parameter field.

                This will be used to extract the data and for the generated AsyncAPI.
                It is particularly useful when you can't use the name you want because it
                is a Python reserved keyword or similar.
                """
            ),
        ] = None,
        alias_priority: Annotated[
            int | None,
            Doc(
                """
                Priority of the alias. This affects whether an alias generator is used.
                """
            ),
        ] = None,
        validation_alias: Annotated[
            str | None,
            Doc(
                """
                'Whitelist' validation step. The parameter field will be the single one
                allowed by the alias or set of aliases defined.
                """
            ),
        ] = None,
        serialization_alias: Annotated[
            str | None,
            Doc(
                """
                'Blacklist' validation step. The vanilla parameter field will be the
                single one of the alias' or set of aliases' fields and all the other
                fields will be ignored at serialization time.
                """
            ),
        ] = None,
        title: Annotated[
            str | None,
            Doc(
                """
                Human-readable title.
                """
            ),
        ] = None,
        description: Annotated[
            str | None,
            Doc(
                """
                Human-readable description.
                """
            ),
        ] = None,
        examples: Annotated[
            list[Any] | None,
            Doc(
                """
                Example values for this field.
                """
            ),
        ] = None,
        gt: Annotated[
            float | None,
            Doc(
                """
                Greater than. If set, value must be greater than this. Only applicable to
                numbers.
                """
            ),
        ] = None,
        ge: Annotated[
            float | None,
            Doc(
                """
                Greater than or equal. If set, value must be greater than or equal to
                this. Only applicable to numbers.
                """
            ),
        ] = None,
        lt: Annotated[
            float | None,
            Doc(
                """
                Less than. If set, value must be less than this. Only applicable to numbers.
                """
            ),
        ] = None,
        le: Annotated[
            float | None,
            Doc(
                """
                Less than or equal. If set, value must be less than or equal to this.
                Only applicable to numbers.
                """
            ),
        ] = None,
        multiple_of: Annotated[
            float | None,
            Doc(
                """
                Value must be a multiple of this. Only applicable to numbers.
                """
            ),
        ] = Undefined,
        strict: Annotated[
            bool | None,
            Doc(
                """
                If `True`, strict validation is applied to the field.
                """
            ),
        ] = Undefined,
        min_length: Annotated[
            int | None,
            Doc(
                """
                Minimum length for strings.
                """
            ),
        ] = None,
        max_length: Annotated[
            int | None,
            Doc(
                """
                Maximum length for strings.
                """
            ),
        ] = None,
        pattern: Annotated[
            str | None,
            Doc(
                """
                RegEx pattern for strings.
                """
            ),
        ] = None,
        allow_inf_nan: Annotated[
            bool | None,
            Doc(
                """
                If `True`, strict validation is applied to the field.
                """
            ),
        ] = Undefined,
        max_digits: Annotated[
            int | None,
            Doc(
                """
                Maximum number of allow digits for strings.
                """
            ),
        ] = Undefined,
        decimal_places: Annotated[
            int | None,
            Doc(
                """
                Maximum number of decimal places allowed for numbers.
                """
            ),
        ] = Undefined,
        union_mode: Annotated[
            Literal["smart", "left_to_right"] | None,
            Doc(
                """
                The strategy to apply when validating a union. Can be `smart` 
                (the default), or `left_to_right`.
                """
            ),
        ] = None,
        discriminator: Annotated[
            str | None,
            Doc(
                """
                Parameter field name for discriminating the type in a tagged union.
                """
            ),
        ] = None,
        json_schema_extra: Annotated[
            dict[str, Any] | Callable[[dict[str, Any]], None] | None,
            Doc(
                """
                Any additional JSON schema data for the schema property.
                """
            ),
        ] = None,
    ):
        kwargs = dict(
            default=default,
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
