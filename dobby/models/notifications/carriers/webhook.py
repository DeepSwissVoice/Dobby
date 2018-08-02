import logging
from typing import Any, Dict

import requests

from ..carrier import Carrier, carrier
from ..notification import Notification
from ....utils import filter_dict

log = logging.getLogger(__name__)


@carrier("webhook")
class WebhookCarrier(Carrier):
    url: str
    username: str = "Dobby"

    def build_message(self, notification: Notification) -> Dict[str, Any]:
        attachments = []
        for embed in notification.embeds:
            fields = []
            for field in embed.fields:
                fields.append(filter_dict({
                    "title": field.title,
                    "value": field.value,
                    "short": True
                }))

            attachment = {
                "title": embed.title,
                "text": embed.text,
                "color": embed.level.value,
                "footer": embed.footer,
                "fields": fields
            }
            attachments.append(filter_dict(attachment))
        return filter_dict({
            "username": self.username,
            "text": notification.text,
            "attachments": attachments
        })

    def deliver(self, notification: Notification) -> bool:
        data = self.build_message(notification)
        log.debug(data)
        resp = requests.post(self.url, json=data)
        resp.raise_for_status()
        return resp.status_code == 200
