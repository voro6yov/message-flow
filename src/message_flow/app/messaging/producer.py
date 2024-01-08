import abc
from typing import Annotated, Protocol

from typing_extensions import Doc

from ...utils import external


@external
class MessageProducer(Protocol):
    """
    Interface for message producers used to integrate various messaging technologies
    into the Message Flow.
    """

    @abc.abstractmethod
    def send(
        self,
        channel: Annotated[str, Doc("The channel to which the message will be sent.")],
        payload: Annotated[bytes, Doc("The message payload.")],
        headers: Annotated[dict[str, str] | None, Doc("The message headers.")] = None,
    ) -> None:
        """
        Send the message payload and headers to the specified channel.
        """
        pass

    @abc.abstractmethod
    def close(self) -> None:
        """
        Free allocated resources.
        """
        pass
