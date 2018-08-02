from typing import Any

from .converter import converter
from ..config import DictContainer, ListContainer


@converter(dict)
def dict_converter(arg: Any, **kwargs) -> dict:
    if isinstance(arg, DictContainer):
        return arg.to_normal()
    return dict(arg)


@converter(list)
def list_converter(arg: Any, **kwargs) -> list:
    if isinstance(arg, ListContainer):
        return arg.to_normal()
    return list(arg)
