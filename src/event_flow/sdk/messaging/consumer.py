import abc
from typing import Callable, Protocol

from ..utils import export


@export
class MessageConsumer(Protocol):
    @abc.abstractmethod
    def subscribe(self, channels: set[str], handler: Callable[[bytes, dict[str, str]], None]) -> None:
        pass

    @abc.abstractmethod
    def start_consuming(self) -> None:
        pass

    @abc.abstractmethod
    def close(self) -> None:
        pass
