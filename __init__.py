import sys
from logging import getLogger
from logging.config import dictConfig


DEFAULT_LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'default': {
            'format': '[%(asctime)s %(levelname)s %(name)s] %(message)s'
        },
        'json': {
            'class': 'pythonjsonlogger.jsonlogger.JsonFormatter',
            'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        }
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'formatter': 'json',
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'pokerstats': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': True
        },
    }
}

dictConfig(DEFAULT_LOGGING)
L = getLogger(__name__)


def log_unhandled_error(exc_type, exc_value, exc_traceback):
    L.error("Uncaught exception", exc_info=(exc_type, exc_value, exc_traceback))


sys.excepthook = log_unhandled_error
