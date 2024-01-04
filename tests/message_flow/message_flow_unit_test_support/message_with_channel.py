from dataclasses import dataclass
from typing import Any


@dataclass
class MessageWithChannel:
    channel: str
    payload: bytes
    headers: dict[str, Any]
    checked: bool = False

    @property
    def message_type(self) -> str | None:
        return self.headers.get("message-type")

    def mark_checked(self) -> None:
        self.checked = True
