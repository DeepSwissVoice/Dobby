import logging
from contextlib import suppress
from json import JSONDecodeError
from typing import Any, Dict

import requests
from requests import Response

from .. import Context, Group, slave

log = logging.getLogger(__name__)


class Resp:
    response: Response
    json: Dict[str, Any]

    def __init__(self, response: Response):
        self.response = response
        json = None
        with suppress(JSONDecodeError):
            json = response.json()

        self.json = json

    def __getattr__(self, item: str) -> Any:
        return getattr(self.response, item)


class Network:
    @slave()
    def get_url(self, ctx: Context, url: str, params: dict = None) -> Resp:
        log.debug(f"requesting url \"{url}\" with params: {params}")
        resp = requests.get(url, params)
        return Resp(resp)


def setup(dobby: Group):
    dobby.add_ext(Network())
