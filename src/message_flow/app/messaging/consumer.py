import abc
from typing import Annotated, Callable, Protocol

from typing_extensions import Doc

from ...utils import external


@external
class MessageConsumer(Protocol):
    """
    Interface for message consumers used to integrate various messaging technologies
    into the Message Flow.
    """

    @abc.abstractmethod
    def subscribe(
        self,
        channels: Annotated[set[str], Doc("The set of channels to which the consumer should subscribe.")],
        handler: Annotated[
            Callable[[bytes, dict[str, str]], None],
            Doc("The handler utilized for processing messages from specified channels."),
        ],
    ) -> None:
        """
        Subscribe the message consumer to the specified channels, and a handler
        will be used to process the consumed messages.
        """
        pass

    @abc.abstractmethod
    def start_consuming(self) -> None:
        """
        Start consuming messages from the specified channels.
        """
        pass

    @abc.abstractmethod
    def close(self) -> None:
        """
        Free allocated resources.
        """
        pass
