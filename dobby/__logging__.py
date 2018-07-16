import sys

CONFIG = {
    "version": 1,
    "formatters": {
        "default": {
            "()": "colorlog.ColoredFormatter",
            "format": "[{asctime}] {log_color}{levelname} in {module}{reset}: {message}",
            "style": "{"
        }
    },
    "handlers": {
        "stream": {
            "class": "logging.StreamHandler",
            "formatter": "default"
        }
    },
    "root": {
        "level": "NOTSET",
        "handlers": ["stream"]
    }
}

sys.modules[__name__] = CONFIG
