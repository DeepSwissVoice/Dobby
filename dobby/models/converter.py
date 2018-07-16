import abc
from typing import Any

from ..config import DictContainer, ListContainer


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
