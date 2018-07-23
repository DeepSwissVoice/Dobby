import abc
import logging
import typing
from typing import Optional, TYPE_CHECKING, Type

from .notification import Notification
from ..converter import convert
from ...errors import SetupError
from ...utils import SubclassMount

if TYPE_CHECKING:
    from .manager import Manager

log = logging.getLogger(__name__)

CarrierMeta = type("CarrierMeta", (SubclassMount, abc.ABCMeta), {})


class Carrier(metaclass=CarrierMeta):
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


def get_carrier(name: str) -> Optional[Type[Carrier]]:
    name = name.lower()
    for carrier in getattr(Carrier, "_subcls"):
        carrier_name = carrier.__name__.lower()
        names = {carrier_name, carrier_name.replace("carrier", "")}
        if name in names:
            return carrier
