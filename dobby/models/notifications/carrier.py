import abc
import logging
import typing
from functools import partial
from typing import Iterable, Optional, TYPE_CHECKING, Type

from .notification import Notification
from ..converter import convert
from ...errors import SetupError

if TYPE_CHECKING:
    from .manager import Manager

log = logging.getLogger(__name__)

CARRIER_MAP = {}


class Carrier(abc.ABC):
    def __init__(self, manager: "Manager", options: dict):
        self.manager = manager
        self.options = options

        hints = typing.get_type_hints(type(self))
        input_args = options.copy()
        for key, converter in hints.items():
            if key not in input_args:
                if hasattr(self, key):
                    continue
                else:
                    raise SetupError(f"{self} requires key \"{key}\" to be passed",
                                     hint="Make sure you're passing all the required arguments to the Carrier")

            _value = input_args.pop(key)
            value = convert(converter, _value, arguments=options, carrier=self)
            setattr(self, key, value)

        self.init()
        log.info(f"{self} setup!")

    def __repr__(self) -> str:
        return f"<{type(self).__name__}>"

    def init(self):
        pass

    @abc.abstractmethod
    def deliver(self, notification: Notification) -> bool:
        pass


def register_carrier(_carrier: Type[Carrier], aliases: Iterable[str]) -> Type[Carrier]:
    if not issubclass(_carrier, Carrier):
        raise SetupError(f"Carrier must be a subclass of Carrier, not {type(_carrier)}",
                         hint="Make sure your Carriers derive from the class \"Carrier\"!")

    for alias in aliases:
        alias = alias.lower()
        if alias in CARRIER_MAP:
            raise SetupError(f"Can't register {_carrier}, alias \"{alias}\" already exists!",
                             hint="Make sure not to reuse pre-existing aliases for your Carrier!")
        CARRIER_MAP[alias] = _carrier
    return _carrier


def carrier(*aliases: str):
    return partial(register_carrier, aliases=aliases)


def find_carrier(name: str) -> Optional[Type[Carrier]]:
    name = name.lower()
    return CARRIER_MAP.get(name)
