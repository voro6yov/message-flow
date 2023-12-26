from typing import TypedDict

from ..utils import external
from .correlation_id import CorrelationId
from .message_trait import MessageTrait


@external
class MessageInfo(TypedDict, total=False):
    correlation_id: CorrelationId
    title: str
    summary: str
    description: str
    trait: list[MessageTrait]
