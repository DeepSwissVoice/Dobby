import importlib
import logging
from pathlib import Path
from typing import Callable

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


def filter_dict(d: dict, cond: Callable = bool) -> dict:
    return {key: value for key, value in d.items() if cond(value)}


def human_timedelta(s: int) -> str:
    if s >= 2592000:
        return f"{round(s / 2592000)} month(s)"
    if s >= 86400:
        return f"{round(s / 86400)} day(s)"
    if s >= 3600:
        return f"{round(s / 3600)} hour(s)"
    elif s >= 300:
        return f"{round(s / 60)} minute(s)"
    else:
        return f"{round(s)} second(s)"
