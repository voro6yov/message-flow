from enum import Enum

from ...utils import export


@export
class ActionType(Enum):
    SEND = "send"
    RECEIVE = "receive"
