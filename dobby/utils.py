import importlib
import logging
from pathlib import Path
from typing import Callable, Union

from raven import Client
from raven.handlers.logging import SentryHandler

from . import __version__


def setup_sentry():
    """Starts `Sentry` and attaches the `SentryHandler` to `Dobby`'s logger."""
    client = Client(release=__version__)
    handler = SentryHandler(client)
    handler.setLevel(logging.ERROR)
    logging.getLogger(__package__).addHandler(handler)


def find_extensions(fp: str, pkg: str) -> list:
    """Find and load extensions in the directory of *fp*.

    This function is used by `Dobby` to load its own `Slave`s.

    Args:
        fp: File path to search from (__file__)
        pkg: Package to use as reference for importing (__package__)

    Returns:
        A list of modules that have a setup attribute.
    """
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


def filter_dict(d: dict, cond: Callable = bool) -> dict:
    """Filter a `dict` using a condition *cond*.

    Args:
        d: `dict` to filter
        cond: `Callable` which will be called for every value in the
            dictionary to determine whether to filter out the key.
            Defaults to a truthy check.

    Returns:
        A new dictionary consisting of only the keys whose values
        returned a truthy value when ran through the *cond* function.
    """
    return {key: value for key, value in d.items() if cond(value)}


MINUTE_SEC = 60
HOUR_SEC = MINUTE_SEC * 60
DAY_SEC = HOUR_SEC * 24
MONTH_SECONDS = DAY_SEC * 30

_FIVE_MINUTE_SEC = 5 * MINUTE_SEC


def human_timedelta(s: Union[int, float]) -> str:
    """Convert a timedelta from seconds into a string using a more sensible unit.

    Args:
        s: Amount of seconds

    Returns:
        A string representing `s` seconds in an easily understandable way
    """
    if s >= MONTH_SECONDS:
        return f"{round(s / MONTH_SECONDS)} month(s)"
    if s >= DAY_SEC:
        return f"{round(s / DAY_SEC)} day(s)"
    if s >= HOUR_SEC:
        return f"{round(s / HOUR_SEC)} hour(s)"
    elif s >= _FIVE_MINUTE_SEC:
        return f"{round(s / MINUTE_SEC)} minute(s)"
    else:
        return f"{round(s)} second(s)"
