from event_flow.utils import export

from .header_not_found import HeaderNotFound
from .message import Message


@export
class MessageImpl(Message):
    def __init__(self, payload: str, headers: dict[str, str]) -> None:
        self._payload = payload
        self._headers = headers

    def __str__(self) -> str:
        return f"<MessageImpl> id: {self.id}, payload: {self.payload}, headers: {self.headers}"

    def __repr__(self) -> str:
        return f"<MessageImpl> id: {self.id}, payload: {self.payload}, headers: {self.headers}"

    @property
    def id(self) -> str:
        return self.get_required_header(self.ID)

    @property
    def payload(self) -> str:
        return self._payload

    @payload.setter
    def payload(self, payload: str) -> None:
        self._payload = payload

    @property
    def headers(self) -> dict[str, str]:
        return self._headers

    @headers.setter
    def headers(self, headers: dict[str, str]) -> None:
        self._headers = headers

    def get_header(self, name: str) -> str | None:
        return self._headers.get(name)

    def get_required_header(self, name: str) -> str:
        if (value := self._headers.get(name)) is None:
            raise HeaderNotFound(f"No such header: {name} in this message {self}")

        return value

    def has_header(self, name: str) -> bool:
        return name in self._headers

    def set_header(self, name: str, value: str) -> None:
        self._headers[name] = value

    def remove_header(self, name: str) -> None:
        del self._headers[name]
