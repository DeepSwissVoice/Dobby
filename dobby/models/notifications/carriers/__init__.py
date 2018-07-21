import importlib
import logging
from pathlib import Path

log = logging.getLogger(__name__)


def load_all():
    here = Path(__file__)
    files = here.parent.glob("*.py")
    for file in files:
        if file == here:
            continue
        importlib.import_module("." + file.stem, __package__)
        log.debug(f"loaded carrier {file.stem}")
