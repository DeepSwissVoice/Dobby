import abc
import inspect
import logging
from typing import Any, Union

from ..config import DictContainer, ListContainer

log = logging.getLogger(__name__)


class Converter(abc.ABC):
    @abc.abstractmethod
    def convert(self, arg: Any, **kwargs) -> Any:
        pass


class DictConverter(Converter):
    def convert(self, arg: Any, **kwargs) -> dict:
        if isinstance(arg, DictContainer):
            return arg.to_normal()
        return dict(arg)


class ListConverter(Converter):
    def convert(self, arg: Any, **kwargs) -> list:
        if isinstance(arg, ListContainer):
            return arg.to_normal()
        return list(arg)


CONVERTER_MAP = {
    dict: DictConverter,
    list: ListConverter
}


def convert(converter, arg, **kwargs):
    origin = getattr(converter, "__origin__", False)
    if origin:
        if origin is Union:
            types = getattr(converter, "__args__")
            if isinstance(arg, types):
                return arg
            else:
                for _type in types:
                    last_exc = None
                    try:
                        return convert(_type, arg, **kwargs)
                    except Exception as e:
                        e.__cause__ = last_exc
                        last_exc = e
                        log.debug(f"Couldn't coerce {arg} to {_type}")
                    raise TypeError(f"Couldn't convert {arg} to any of {converter}") from last_exc

    if converter in CONVERTER_MAP:
        converter = CONVERTER_MAP[converter]

    if inspect.isclass(converter):
        if issubclass(converter, Converter):
            inst = converter()
            return inst.convert(arg, **kwargs)
        elif hasattr(converter, "convert") and inspect.ismethod(converter.convert):
            return converter.convert(arg, **kwargs)
    elif isinstance(converter, Converter):
        return converter.convert(arg, **kwargs)

    return converter(arg)
