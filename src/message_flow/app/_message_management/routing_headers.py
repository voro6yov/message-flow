from ...utils import internal


@internal
class RoutingHeaders:
    TYPE: str = "message-type"
    ADDRESS: str = "channel-address"
    REPLY_TO: str = "reply-to-address"
