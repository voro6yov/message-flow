from ..message import Message
from ..utils import internal


@internal
class OperationReply:
    def __init__(self, channel: str | None, message: type[Message] | None) -> None:
        self.channel = channel
        self.message = message

    @property
    def is_provided(self) -> bool:
        return self.channel is not None and self.message is not None

    @property
    def is_valid(self) -> bool:
        return not (
            (self.message is not None and self.channel is None) or (self.message is None and self.channel is not None)
        )
