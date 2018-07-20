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


def find_extensions(fp: str, pkg: str) -> list:
    file = Path(fp)
    exts = []
    for child in file.parent.iterdir():
        if child == file:
            continue
        import_name = "." + child.stem
        mod = importlib.import_module(import_name, pkg)
        if hasattr(mod, "setup"):
            exts.append(mod)
    return exts


class SubclassMount(type):

    def __init__(cls, name, bases, attrs):
        if not hasattr(cls, "_subcls"):
            cls._subcls = []
            return
        cls._subcls.append(cls)
