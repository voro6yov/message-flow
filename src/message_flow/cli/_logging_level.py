from enum import Enum
from typing import final

from ..utils import internal


@final
@internal
class LoggingLevel(str, Enum):
    CRITICAL = "critical"
    ERROR = "error"
    WARNING = "warning"
    INFO = "info"
    DEBUG = "debug"
