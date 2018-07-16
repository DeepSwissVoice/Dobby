import abc
from typing import Any


class Converter(abc.ABC):
    @abc.abstractmethod
    def convert(self, arg: Any, **kwargs) -> Any:
        pass
