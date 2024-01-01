from typing import final

from ..utils import internal


@final
@internal
class Reference:
    """
    A simple object to allow referencing other components in the app,
    internally and externally.
    """

    def __init__(self, id: str, reference: str) -> None:
        self.id = id
        self.reference = reference

    @classmethod
    def for_channel(cls, channel_id: str) -> "Reference":
        return cls(channel_id, f"/channels/{channel_id}")

    @classmethod
    def for_operation(cls, operation_id: str) -> "Reference":
        return cls(operation_id, f"/operations/{operation_id}")

    @classmethod
    def for_message(cls, message_id: str) -> "Reference":
        return cls(message_id, f"/messages/{message_id}")

    def as_link(self) -> dict[str, str]:
        return {"$ref": f"#{self.reference}"}

    def as_component(self) -> dict[str, dict[str, str]]:
        return {self.id: {"$ref": f"#/components{self.reference}"}}

    def as_direct_component(self) -> dict[str, str]:
        return {"$ref": f"#/components{self.reference}"}

    def merge(self, other: "Reference") -> "Reference":
        return Reference(other.id, f"{self.reference}{other.reference}")
