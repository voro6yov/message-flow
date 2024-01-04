import logging

from .app import *
from .channel import *
from .message import *

__all__ = app.__all__ + channel.__all__ + message.__all__

logger = logging.getLogger(__name__)

ch = logging.StreamHandler()
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
ch.setFormatter(formatter)
logger.addHandler(ch)
