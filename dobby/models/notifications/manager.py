import logging
from typing import List

from .carrier import Carrier, find_carrier
from .notification import Notification
from ...errors import SetupError

log = logging.getLogger(__name__)


class Manager:
    carriers: List[Carrier]

    def __init__(self, carriers: List[Carrier] = None):
        self.carriers = carriers or []

    @classmethod
    def load(cls, config: dict) -> "Manager":
        inst = cls()

        for key, value in config.items():
            carrier_cls = find_carrier(key)
            if not carrier_cls:
                raise SetupError(f"Couldn't find carrier \"{key}\"",
                                 hint="Check whether the name is spelled correctly and, "
                                      "if the carrier belongs to an extension, check whether the extension is loaded")

            if not isinstance(value, list):
                value = [value]

            for sub_value in value:
                carrier = carrier_cls(inst, sub_value)
                inst.carriers.append(carrier)

        return inst

    def send(self, notification: Notification):
        for carrier in self.carriers:
            exc = None

            try:
                delivered = carrier.deliver(notification)
            except Exception as e:
                exc = e
                delivered = False

            if not delivered:
                log.warning(f"{carrier} failed to deliver {notification} ({exc})")
