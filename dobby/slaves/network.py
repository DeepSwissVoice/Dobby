import logging
from typing import Dict

import requests
from requests import Response

from ..models import Context, slave

__all__ = ["get_url"]

log = logging.getLogger(__name__)


@slave
def get_url(ctx: Context, url: str, params: Dict[str, str] = None) -> Response:
    log.debug(f"requesting url \"{url}\" with params: {params}")
    return requests.get(url, params)
