import copy
import enum
from typing import Callable


def unwrap(func: Callable) -> Callable:
    def wrapper(kwargs):
        return func(**kwargs)

    return wrapper


class ColorLevel(enum.Enum):
    INFO = "#64FFDF"
    SUCCESS = "#46FF38"
    WARNING = "#FFC94C"
    ERROR = "#FF4438"


def iter_format(inst, *args, **kwargs):
    if isinstance(inst, str):
        return inst.format(*args, **kwargs)
    elif isinstance(inst, list):
        for i, value in enumerate(inst):
            inst[i] = iter_format(value, *args, **kwargs)
    elif isinstance(inst, dict):
        for key in inst:
            inst[key] = iter_format(inst[key], *args, **kwargs)
    elif isinstance(inst, _Container):
        for key, value in vars(inst).items():
            new_value = iter_format(value, *args, **kwargs)
            if new_value is not value:
                setattr(inst, key, new_value)
    return inst


class _Container:
    def copy(self) -> "_Container":
        container = object.__new__(type(self))
        for key, value in vars(self).items():
            if isinstance(value, _Container):
                value = value.copy()
            else:
                value = copy.copy(value)
            setattr(container, key, value)
        return container

    def format_all(self, *args, __copy=True, **kwargs) -> "_Container":
        inst = self.copy() if __copy else self
        iter_format(inst, *args, **kwargs)
        return inst


class Field(_Container):
    def __init__(self, **kwargs):
        self.title = kwargs.get("title")
        self.value = kwargs.get("value")


class Embed(_Container):
    def __init__(self, *fields, **kwargs):
        self.title = kwargs.get("title")
        _level = kwargs.get("level", "INFO")
        self.level = ColorLevel[_level] if not isinstance(_level, ColorLevel) else _level
        self.text = kwargs.get("text")
        self.footer = kwargs.get("footer")

        _fields = fields or kwargs.get("fields", [])
        if isinstance(_fields, dict):
            self.fields = [Field(title=key, value=value) for key, value in _fields.items()]
        else:
            self.fields = list(map(unwrap(Field), _fields))


class Notification(_Container):
    def __init__(self, *embeds, **kwargs):
        self.text = kwargs.get("text")
        self.embeds = list(map(unwrap(Embed), embeds or kwargs.get("embeds", [])))

    @classmethod
    def from_exception(cls, exc: Exception) -> "Notification":
        pass
