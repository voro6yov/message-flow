import json
import sys
from types import FunctionType
from typing import Annotated, Any, Type

from pydantic import BaseModel, create_model
from pydantic.fields import FieldInfo
from pydantic_core import PydanticUndefined
from typing_extensions import dataclass_transform

from ...utils import export
from .header import Header
from .payload import Payload


@export
@dataclass_transform(kw_only_default=True, field_specifiers=(Header, Payload))
class Message:
    def __new__(cls, *args, **kwargs) -> "Message":
        cls.MethodGenerator(cls).generate_init()

        return super().__new__(cls)

    @property
    def headers(self) -> dict[str, str]:
        if not hasattr(self, "_headers"):
            headers_model = self.make_headers_model()
            self._headers = headers_model(
                **{header_name: getattr(self, header_name) for header_name in self._get_attribute_names_for(Header)}
            ).model_dump()

        return self._headers

    @property
    def payload(self) -> bytes:
        if not hasattr(self, "_payload"):
            payload_model = self.make_payload_model()
            self._payload = (
                payload_model(
                    **{
                        payload_name: getattr(self, payload_name)
                        for payload_name in self._get_attribute_names_for(Payload)
                    }
                )
                .model_dump_json()
                .encode()
            )
        return self._payload

    @property
    def type(self) -> str:
        return self.__class__.__name__

    @classmethod
    def make_headers_model(cls) -> BaseModel:
        header_props = (
            (
                header_name,
                cls.__annotations__[header_name],
                cls.__dict__[header_name],
            )
            for header_name in cls._get_attribute_names_for(Header)
        )
        return create_model(
            "headers",
            **{
                header_name: (Annotated[header_type, header], header.default)
                for header_name, header_type, header in header_props
            },
        )

    @classmethod
    def make_payload_model(cls) -> BaseModel:
        payload_props = (
            (
                payload_name,
                cls.__annotations__[payload_name],
                cls.__dict__[payload_name],
            )
            for payload_name in cls._get_attribute_names_for(Payload)
        )
        return create_model(
            "payload",
            **{
                payload_name: (
                    Annotated[payload_type, payload],
                    payload.default,
                )
                for payload_name, payload_type, payload in payload_props
            },
        )

    @classmethod
    def from_payload_and_headers(cls, raw_payload: bytes, headers: dict[str, str]) -> "Message":
        payload: dict[str, str] = json.loads(raw_payload.decode())
        return cls(
            **payload,
            **{
                header_name: header
                for header_name in cls._get_attribute_names_for(Header)
                if (header := headers.get(header_name)) is not None
            },
        )

    def add_headers(self, extra_headers: dict[str, str]) -> None:
        self.headers.update(extra_headers)

    @classmethod
    def _get_attribute_names_for(cls, attribute_type: Type[Header | Payload]) -> list[str]:
        return [
            attribute_name
            for attribute_name in cls.__dict__
            if not attribute_name.startswith("__")
            and not attribute_name.endswith("__")
            and isinstance(cls.__dict__[attribute_name], attribute_type)
        ]

    class MethodGenerator:
        def __init__(self, cls: Type["Message"]) -> None:
            self.cls = cls

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

        def _check_argument_order(self) -> None:
            seen_default = False
            for component_name, component in self.components.items():
                if component.default is not None:
                    seen_default = True
                elif seen_default:
                    raise RuntimeError(f"Non-default attribute {component_name!r} follows default attribute.")

        def _make_body(self) -> str:
            body_lines = []

            for component_name, component in self.components.items():
                default_name = f"_dflt_{component_name}"
                if component.default is not None:
                    self.globals[default_name] = component.default

                value = component_name

                body_lines.append(f"self.{component_name} = {value}")

            if not body_lines:
                body_lines = ["pass"]

            return "\n".join(f"  {b}" for b in body_lines)

        def _make_args(self) -> str:
            init_params = []
            for component_name, component in self.components.items():
                if component.default is None or component.default == PydanticUndefined:
                    default = ""
                else:
                    default = f" = _dflt_{component_name}"

                init_params.append(f"{component_name}: _type_{component_name}{default}")

            return ", ".join(["self", "*"] + init_params)

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
                return

            self._check_argument_order()

            setattr(self.cls, "__init__", self._make_constructor())
