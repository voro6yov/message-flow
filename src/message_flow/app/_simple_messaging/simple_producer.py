import json
import logging
from typing import final

from ...utils import internal
from ..messaging import MessageProducer


@final
@internal
class SimpleMessageProducer(MessageProducer):
    def __init__(self, logger: logging.Logger, file_path: str = "/tmp/message-flow-queue.txt") -> None:
        self._logger = logger

        self.closed = False

        self._file_path = file_path

    def send(self, channel: str, payload: bytes, headers: dict[str, str] | None = None) -> None:
        self._logger.debug(f"Send message to {channel}")
        with open(self._file_path, "a+") as fp:
            fp.write(f"{channel}\t{payload.decode()}\t{json.dumps(headers)}\n")

    def close(self) -> None:
        self.closed = True
