import json
import logging
import time
from typing import Callable, final

from ...utils import internal
from ..messaging import MessageConsumer


@final
@internal
class SimpleMessageConsumer(MessageConsumer):
    def __init__(self, file_path: str = "/tmp/message-flow-queue.txt") -> None:
        self._logger = logging.getLogger(__name__)

        self._fp = open(file_path, "r+")
        self._router = {}

        self._initialize()

    def subscribe(self, channels: set[str], handler: Callable[[bytes, dict[str, str]], None]) -> None:
        for channel in channels:
            self._router[channel] = handler

    def start_consuming(self) -> None:
        self._logger.info("Start consuming")

        while True:
            message = self._get_message()
            self._process_message(message)

    def close(self) -> None:
        return self._fp.close()

    def _initialize(self) -> None:
        self._fp.seek(0, 2)
        self._position = self._fp.tell()

    def _get_message(self) -> str | None:
        return self._fp.readline() or None

    def _process_message(self, message: str | None) -> None:
        try:
            if message is not None:
                self._handle_message(message)

            time.sleep(1)
        except Exception as error:
            self._logger.info("An error occurred while consuming events", exc_info=error)
        finally:
            self._commit_message(message)

    def _handle_message(self, message: str) -> None:
        channel, payload, headers = self._parse_message(message)

        if (handler := self._router.get(channel)) is None:
            self._logger.warning(f"Received message for unknown channel {channel}")
            return

        handler(payload, headers)

    def _parse_message(self, message: str) -> tuple[str, bytes, dict[str, str]]:
        channel, payload, headers = message.strip().split("\t")
        return channel, payload.encode(), json.loads(headers)

    def _commit_message(self, message: str | None) -> None:
        if message is not None:
            self._position += len(message)
            self._fp.seek(self._position)
