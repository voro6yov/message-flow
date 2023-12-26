from typing import final

from ..utils import external


@final
@external
class CorrelationId:
    """
    An object that specifies an identifier at design time that can used for message tracing and correlation.
    """

    description: str | None
    location: str

    def __init__(self, location: str, description: str | None = None) -> None:
        self.description = description
        self.location = location

    def is_valid(self, headers: list[str]) -> None:
        if self.location not in headers:
            raise RuntimeError(f"Correlation ID location {self.location!r} not found in message headers.")

    def as_schema(self) -> dict[str, str]:
        schema = {
            "location": f"$message.header#/{self.location}",
        }
        if self.description is not None:
            schema["description"] = self.description

        return schema
