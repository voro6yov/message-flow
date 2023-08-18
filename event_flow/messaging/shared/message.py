from abc import abstractmethod
from typing import Protocol

from event_flow.utils import export


@export
class Message(Protocol):
    ID: str = "ID"
    PARTITION_ID: str = "PARTITION_ID"
    DESTINATION: str = "DESTINATION"
    DATE: str = "DATE"

    @property
    @abstractmethod
    def id(self) -> str:
        ...

    @property
    @abstractmethod
    def payload(self) -> str:
        ...

    @property
    @abstractmethod
    def headers(self) -> dict[str, str]:
        ...

    @abstractmethod
    def get_header(self, name: str) -> str | None:
        ...

    @abstractmethod
    def get_required_header(self, name: str) -> str:
        ...

    @abstractmethod
    def has_header(self, name: str) -> bool:
        ...

    @abstractmethod
    def set_header(self, name: str, value: str) -> None:
        ...

    @abstractmethod
    def remove_header(self, name: str) -> None:
        ...
