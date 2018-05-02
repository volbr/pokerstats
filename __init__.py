import sys
from logging import getLogger
from logging.config import dictConfig


__version__ = '1.0.0'
L = getLogger(__name__)

# TODO: dictConfig logging


def log_unhandled_error(exc_type, exc_value, exc_traceback):
    L.error("Uncaught exception", exc_info=(exc_type, exc_value, exc_traceback))


sys.excepthook = log_unhandled_error

__all__ = ['__config__', 'config']
