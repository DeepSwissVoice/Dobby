import importlib
import logging
from pathlib import Path

from raven import Client
from raven.handlers.logging import SentryHandler

from . import __version__


def setup_sentry():
    client = Client(release=__version__)
    handler = SentryHandler(client)
    handler.setLevel(logging.ERROR)
    logging.getLogger(__package__).addHandler(handler)


def find_extensions(file: Path) -> list:
    exts = []
    for child in file.parent.iterdir():
        if child == file:
            continue
        import_name = ".".join((*child.parts[:-1], child.stem))
        mod = importlib.import_module(import_name)
        if hasattr(mod, "setup"):
            exts.append(mod)
    return exts
