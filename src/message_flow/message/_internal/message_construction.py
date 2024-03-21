import sys
from abc import ABCMeta
from types import FunctionType
from typing import TYPE_CHECKING, Any, final

from pydantic.fields import FieldInfo
from pydantic_core import PydanticUndefined
from typing_extensions import dataclass_transform

from ...shared import Components, Reference
from ..header import Header
from ..payload import Payload
from .message_schema import MessageSchema

if TYPE_CHECKING:
    from ..message import Message
    from ..message_trait import MessageTrait

from ...utils import internal


@final
@internal
@dataclass_transform(kw_only_default=True, field_specifiers=(Header, Payload))
class MessageMeta(ABCMeta):
    def __new__(mcs, name, bases, namespace, **kwargs):
        if bases:
            mcs.process_traits(namespace)

            cls: type[Message] = super().__new__(mcs, name, bases, namespace, **kwargs)

            mcs.MethodGenerator(cls).generate_init()
            mcs.SchemaGenerator(cls).generate_schema()

            return cls

        return super().__new__(mcs, name, bases, namespace, **kwargs)

    @classmethod
    def process_traits(cls, namespace: dict[str, Any]) -> None:
        if namespace.get("message_info") is None:
            return

        traits: list[MessageTrait] = namespace["message_info"].pop("traits", [])

        for trait in traits:
            trait.update_headers(namespace)
            trait.update_message_info(namespace)

    class MethodGenerator:
        def __init__(self, message_class: type["Message"]) -> None:
            self.cls = message_class

            self._globals: dict[str, Any] | None = None
            self._locals: dict[str, Any] | None = None

        @property
        def globals(self) -> dict[str, Any]:
            if self._globals is None:
                self._globals = sys.modules[self.cls.__module__].__dict__ if self.cls.__module__ in sys.modules else {}

            return self._globals

        @property
        def locals(self) -> dict[str, Any]:
            if self._locals is None:
                self._locals = {
                    f"_type_{component_name}": component.annotation
                    for component_name, component in self.components.items()
                }

            return self._locals

        @property
        def components(self) -> dict[str, FieldInfo]:
            if not hasattr(self, "_components"):
                components = {}
                for component_name in self.cls.__dict__:
                    if (
                        not component_name.startswith("__")
                        and not component_name.endswith("__")
                        and isinstance(
                            self.cls.__dict__[component_name],
                            (Header, Payload),
                        )
                    ):
                        field_info: FieldInfo = self.cls.__dict__[component_name]
                        field_info.annotation = self.cls.__annotations__[component_name]
                        components[component_name] = field_info

                self._components: dict[str, FieldInfo] = components

            return self._components

        def _has_constructor(self) -> bool:
            return "__init__" in self.cls.__dict__

        def _make_body(self) -> str:
            body_lines = []

            for component_name, component in self.components.items():
                default_name = f"_dflt_{component_name}"
                if component.default_factory is not None:
                    self.globals[default_name] = component.default_factory
                    value = f"{default_name}() if {component_name} == '_HAS_DEFAULT_FACTORY' else {component_name}"
                else:
                    self.globals[default_name] = component.default
                    value = component_name

                body_lines.append(f"self.{component_name} = {value}")

            if not body_lines:
                body_lines = ["pass"]

            return "\n".join(f"  {b}" for b in body_lines)

        def _make_args(self) -> str:
            init_params = []
            for component_name, component in self.components.items():
                if component.default != PydanticUndefined:
                    default = f" = _dflt_{component_name}"
                elif component.default_factory is not None:
                    default = "='_HAS_DEFAULT_FACTORY'"
                else:
                    default = ""

                init_params.append(f"{component_name}: _type_{component_name}{default}")

            return ", ".join(["self", "*" if init_params else ""] + init_params)

        def _make_return_annotation(self) -> str:
            self.locals["_return_type"] = None
            return " -> _return_type"

        def _make_constructor(self) -> FunctionType:
            init_txt = f" def __init__({self._make_args()}){self._make_return_annotation()}:\n{self._make_body()}"
            create_init_txt = f"def __create_init__({', '.join(self.locals.keys())}):\n{init_txt}\n return __init__"

            ns = {}
            exec(create_init_txt, self.globals, ns)

            constructor = ns["__create_init__"](**self.locals)
            constructor.__qualname__ = f"{self.cls.__qualname__}.{constructor.__name__}"

            return constructor

        def generate_init(self) -> None:
            if self._has_constructor():
                raise RuntimeError("Please do not define explicit constructor.")

            setattr(self.cls, "__init__", self._make_constructor())

    class SchemaGenerator:
        def __init__(self, message_class: type["Message"]) -> None:
            self.cls = message_class

            self._components = Components()
            self._schema = MessageSchema(contentType="application/json")

        @property
        def headers_schema(self) -> dict[str, Any]:
            if not hasattr(self, "_headers_schema"):
                self._headers_schema = self.cls.headers_model().model_json_schema(
                    ref_template="#/components/schemas/{model}"
                )
            return self._headers_schema

        @property
        def payload_schema(self) -> dict[str, Any]:
            if not hasattr(self, "_payload_schema"):
                self._payload_schema = self.cls.payload_model().model_json_schema(
                    ref_template="#/components/schemas/{model}"
                )
            return self._payload_schema

        def generate_schema(self) -> None:
            self._add_reference_schemas()
            self._add_message()
            self._add_async_api_attributes()

        def _add_reference_schemas(self) -> None:
            if "$defs" in self.headers_schema:
                self._components.add_schemas(self.headers_schema.pop("$defs"))

            if "$defs" in self.payload_schema:
                self._components.add_schemas(self.payload_schema.pop("$defs"))

        def _add_message(self) -> None:
            self._add_payload_to_schema()
            self._add_headers_to_schema()
            self._add_correlation_id_to_schema()
            self._add_info_to_schema()

            self._components.add_message(self.cls.__name__, self._schema)  # type: ignore

        def _add_async_api_attributes(self) -> None:
            self.cls.__async_api_reference__ = Reference.for_message(self.cls.__name__)
            self.cls.__async_api_components__ = self._components

        def _add_payload_to_schema(self) -> None:
            self._schema["payload"] = self.payload_schema

        def _add_headers_to_schema(self) -> None:
            self._schema["headers"] = self.headers_schema

        def _add_correlation_id_to_schema(self) -> None:
            if (correlation_id := self.cls.message_info.get("correlation_id")) is not None:
                correlation_id.is_valid(self.cls.headers_attributes())
                self._schema["correlationId"] = correlation_id.as_schema()

        def _add_info_to_schema(self) -> None:
            if (title := self.cls.message_info.get("title")) is not None:
                self._schema["title"] = title
            if (summary := self.cls.message_info.get("summary")) is not None:
                self._schema["summary"] = summary
            if (description := self.cls.message_info.get("description")) is not None:
                self._schema["description"] = description
