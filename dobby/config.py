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


class ListContainer(_Container, UserList):
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
    env: Environment
    ext: ListContainer
    tasks: DictContainer

    def __init__(self, env: Environment, ext: ListContainer, notifications: DictContainer, tasks: DictContainer, data: DictContainer):
        self.env = env
        self.ext = ext
        self.notifications = notifications
        self.tasks = tasks
        super().__init__(data)

    @classmethod
    def load(cls, fp: Path) -> "Config":
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
