from typing import Annotated, final

from typing_extensions import Doc

from ..utils import external


@final
@external
class CorrelationId:
    """
    An object that defines a design-time identifier for message tracing and correlation purposes.

    **Example**

    ```python
    from message_flow import CorrelationId

    correlation_id = CorrelationId("corelation_id")
    ```
    """

    description: str | None
    location: str

    def __init__(
        self,
        location: Annotated[str, Doc("A header name that specifies the location of the correlation ID.")],
        description: Annotated[
            str | None,
            Doc(
                """
                An optional description of the identifier. CommonMark syntax can 
                be used for rich text representation.

                **Example**

                ```python
                from message_flow import CorrelationId

                correlation_id = CorrelationId("corelation_id", "Correlation Id used for tracing.")
                ```
                """
            ),
        ] = None,
    ) -> None:
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
