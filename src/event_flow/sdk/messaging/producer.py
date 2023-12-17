import abc
from typing import Protocol

from ..utils import export


@export
class MessageProducer(Protocol):
    @abc.abstractmethod
    def send(self, channel: str, payload: bytes, headers: dict[str, str] | None = None) -> None:
        pass

    @abc.abstractmethod
    def close(self) -> None:
        pass
