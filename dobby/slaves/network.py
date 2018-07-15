import logging
from typing import Dict

import requests
from requests import Response

from .. import Context, GroupMixin, slave

log = logging.getLogger(__name__)


class Network:
    @slave()
    def get_url(self, ctx: Context, url: str, params: Dict[str, str] = None) -> Response:
        log.debug(f"requesting url \"{url}\" with params: {params}")
        return requests.get(url, params)


def setup(dobby: GroupMixin):
    dobby.add_ext(Network)
