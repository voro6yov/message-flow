from event_flow.utils import export

from .messaging_exception import MessagingException


@export
class HeaderNotFound(MessagingException):
    pass
