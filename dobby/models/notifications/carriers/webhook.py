from typing import Any, Dict

import requests

from ..carrier import Carrier
from ..notification import Notification


class WebhookCarrier(Carrier):
    url: str
    username: str = "Dobby"

    def build_message(self, notification: Notification) -> Dict[str, Any]:
        return {
            "username": self.username,
            "text": notification.text
        }

    def deliver(self, notification: Notification) -> bool:
        data = self.build_message(notification)
        resp = requests.post(self.url, json=data)
        return resp.status_code == 200
