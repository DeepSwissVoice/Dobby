import abc
import os
from ast import literal_eval
from collections import UserDict, UserList
from contextlib import suppress
from pathlib import Path
from typing import Any

import yaml

from .errors import EnvError

_DEFAULT = object()


class _Container(abc.ABC):
    """Base class for `ListContainer` and `DictContainer`

    Provides an access wrapper for `data` and an `Environment`.
    When accessing an item from this Container it tries to get it from
    the data first and if it doesn't find it there it'll get it from the
    `Environment`.

    Attributes:
        env: Reference to the `Environment` that's used.
    """
    env: "Environment"

    def __init__(self, env: "Environment", data, *args, **kwargs):
        self.env = env
        super().__init__(data)

    def __getstate__(self):
        return dict(env=self.env, data=self.data)

    def __setstate__(self, state):
        self.env = state["env"]
        self.data = state["data"]

    def __getitem__(self, item: Any) -> Any:
        return getitem(self.env, super().__getitem__(item))

    @abc.abstractmethod
    def to_normal(self):
        """Convert this Container to its Python equivalent."""
        pass


class ListContainer(_Container, UserList):
    """A list with Environment support."""
    __class__ = list

    data: list

    def __init__(self, env: "Environment", data: list = None):
        super().__init__(env, data)

    def to_normal(self) -> list:
        normal = []
        for el in self.data:
            if isinstance(el, (ListContainer, DictContainer)):
                el = el.to_normal()
            normal.append(el)
        return normal


class DictContainer(_Container, UserDict):
    """A dict with Environment support."""
    __class__ = dict

    data: dict

    def __init__(self, env: "Environment", data: dict = None):
        super().__init__(env, data)

    def __getattr__(self, item: str) -> Any:
        return self.__getitem__(item)

    def to_normal(self) -> dict:
        normal = {}
        for key, val in self.data.items():
            if isinstance(val, (ListContainer, DictContainer)):
                val = val.to_normal()
            normal[key] = val
        return normal


def getitem(env: "Environment", value: Any) -> Any:
    """Wrap value in `Container` or resolve it if it points to an environment variable.

    Args:
        env: `Environment` to use for pointer lookups
        value: Value to resolve

    Returns:
        The actual value
    """
    if isinstance(value, list):
        return ListContainer(env, value)
    elif isinstance(value, dict):
        return DictContainer(env, value)
    elif isinstance(value, str):
        if value.startswith("$"):
            return env[value[1:]]
    return value


# noinspection PyUnreachableCode
def parse_value(value: str) -> Any:
    """Parse a string into an object.

    This function is used to parse environment variables into
    their corresponding Python object.

    Args:
        value: String value to parse

    Returns:
        The parsed value

    Raises:
        `ValueError` when the value couldn't be parsed
    """
    with suppress(SyntaxError, ValueError):
        return literal_eval(value)

    quoted_value = "\"" + value.replace("\"", "\\\"") + "\""
    try:
        return literal_eval(quoted_value)
    except (SyntaxError, ValueError) as e:
        raise ValueError(f"Couldn't parse value {value}") from e


class Environment(DictContainer):
    def __init__(self, data: dict = None):
        super().__init__(self, data)

    def __getitem__(self, item: Any) -> Any:
        """Get the value of key *item*.

        Tries to get the value from the environment variables first
        and if it doesn't exist there it returns the value specified
        in the `env` section of the config file.

        Args:
            item: Key to retrieve

        Returns:
            The value found

        Raises:
            `EnvError` when *item* isn't present or its value couldn't be parsed
        """
        value = os.getenv(str(item), _DEFAULT)
        if value is not _DEFAULT:
            try:
                value = parse_value(value)
            except ValueError:
                raise EnvError(f"Couldn't parse value of key \"{item}\" in environment variables ({value})",
                               hint="Make sure the value is well-formatted!")

            return getitem(self, value)

        try:
            return super().__getitem__(item)
        except KeyError:
            raise EnvError(f"Your env is missing \"{item}\" which is required!",
                           hint="Define it in the config file or set it in the environment variables")


class Config(UserDict):
    """The global config used by `Dobby`.

    It's a `collections.UserDict` subclass specialised for Dobby.

    Attributes:
        env: `Environment` used to resolve pointers parsed
            from the config file
        ext: `ListContainer` of names of extensions named
            in the config file
        notifications: `DictContainer` holding the notification
            configuration
        tasks: `DictContainer` of parsed task configurations
            from the config file
    """
    env: Environment
    ext: ListContainer
    notifications: DictContainer
    tasks: DictContainer

    def __init__(self, env: Environment, ext: ListContainer, notifications: DictContainer, tasks: DictContainer, data: DictContainer):
        self.env = env
        self.ext = ext
        self.notifications = notifications
        self.tasks = tasks
        super().__init__(data)

    @classmethod
    def load(cls, fp: Path) -> "Config":
        """Build a `Config` instance from a `pathlib.Path`.

        Parses the YAML contents of the file and constructs a `Config`.

        Args:
            fp: `pathlib.Path` to read data from

        Returns:
            `Config` based on *fp*
        """
        config = yaml.load(fp.read_text())
        env = Environment(config.pop("env", None))

        _ext = config.pop("ext", None)
        if isinstance(_ext, str):
            _ext = [_ext]
        ext = ListContainer(env, _ext)

        notifications = DictContainer(env, config.pop("notifications", None))
        tasks = DictContainer(env, config.pop("tasks", None))
        data = DictContainer(env, config)

        return cls(env, ext, notifications, tasks, data)
