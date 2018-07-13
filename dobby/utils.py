import logging

from raven import Client
from raven.handlers.logging import SentryHandler

from . import __version__


def setup_sentry():
    client = Client(release=__version__)
    handler = SentryHandler(client)
    handler.setLevel(logging.ERROR)
    logging.getLogger(__package__).addHandler(handler)
