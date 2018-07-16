import os
from ast import literal_eval
from collections import UserDict, UserList
from pathlib import Path
from typing import Any

import yaml

_DEFAULT = object()


class ListContainer(UserList):
    __class__ = list

    env: "Environment"
    data: list

    def __init__(self, env: "Environment", data: list = None):
        self.env = env
        super().__init__(data)

    def __getitem__(self, item: int) -> Any:
        return getitem(self.env, super().__getitem__(item))

    def to_normal(self) -> list:
        normal = []
        for el in self.data:
            if isinstance(el, (ListContainer, DictContainer)):
                el = el.to_normal()
            normal.append(el)
        return normal


class DictContainer(UserDict):
    __class__ = dict

    env: "Environment"
    data: dict

    def __init__(self, env: "Environment", data: dict = None):
        self.env = env
        super().__init__(data)

    def __getattr__(self, item: str) -> Any:
        return self.__getitem__(item)

    def __getitem__(self, item: Any) -> Any:
        return getitem(self.env, super().__getitem__(item))

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


class Environment(DictContainer):
    def __init__(self, data: dict = None):
        super().__init__(self, data)

    def __getitem__(self, item: Any) -> Any:
        value = os.getenv(str(item), _DEFAULT)
        if value is not _DEFAULT:
            value = literal_eval(value)
            return getitem(self, value)
        try:
            return super().__getitem__(item)
        except KeyError:
            raise KeyError(f"Environment is missing \"{item}\" which is required!")


class Config(UserDict):
    env: Environment
    ext: ListContainer
    tasks: DictContainer

    def __init__(self, env: Environment, ext: ListContainer, tasks: DictContainer, data: DictContainer):
        self.env = env
        self.ext = ext
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

        tasks = DictContainer(env, config.pop("tasks", {}))
        data = DictContainer(env, config)

        return cls(env, ext, tasks, data)
