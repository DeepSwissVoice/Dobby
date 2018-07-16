import logging

import requests
from requests import Response

from .. import Context, Group, slave

log = logging.getLogger(__name__)


class Network:
    @slave()
    def get_url(self, ctx: Context, url: str, params: dict = None) -> Response:
        log.debug(f"requesting url \"{url}\" with params: {params}")
        return requests.get(url, params)


def setup(dobby: Group):
    dobby.add_ext(Network())
