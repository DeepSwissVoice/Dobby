import os
from ast import literal_eval
from collections import UserDict, UserList
from typing import Any, TextIO

import yaml

_DEFAULT = object()


class ListContainer(UserList):
    env: "Environment"
    data: list

    def __init__(self, env: "Environment", data: list = None):
        self.env = env
        super().__init__(data)

    def __getitem__(self, item: int) -> Any:
        return getitem(self.env, super().__getitem__(item))


class DictContainer(UserDict):
    env: "Environment"
    data: dict

    def __init__(self, env: "Environment", data: dict = None):
        self.env = env
        super().__init__(data)

    def __getattr__(self, item: str) -> Any:
        return self.__getitem__(item)

    def __getitem__(self, item: Any) -> Any:
        return getitem(self.env, super().__getitem__(item))


def getitem(env: "Environment", value: Any) -> Any:
    if isinstance(value, list):
        return ListContainer(env, value)
    elif isinstance(value, dict):
        return DictContainer(env, value)
    elif isinstance(value, str):
        if value.startswith("$"):
            return env.get(value[1:])
    return value


class Environment(DictContainer):
    def __init__(self, data: dict = None):
        super().__init__(self, data)

    def __getitem__(self, item: Any) -> Any:
        value = os.getenv(str(item), _DEFAULT)
        if value is not _DEFAULT:
            value = literal_eval(value)
            return getitem(self, value)
        return super().__getitem__(item)


class Config(UserDict):
    env: Environment

    def __init__(self, env: Environment, tasks: DictContainer, data: DictContainer):
        self.env = env
        self.tasks = tasks
        super().__init__(data)

    @classmethod
    def load(cls, fp: TextIO) -> "Config":
        config = yaml.load(fp)
        env = Environment(config.pop("env", None))
        tasks = DictContainer(env, config.pop("tasks", {}))
        data = DictContainer(env, config)
        return cls(env, tasks, data)
