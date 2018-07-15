import logging
from pathlib import Path
from typing import TYPE_CHECKING

from .. import Group
from ..utils import find_extensions

if TYPE_CHECKING:
    from .. import Dobby

log = logging.getLogger(__name__)

group = Group(name="dobby")

exts = find_extensions(Path(__file__))
for ext in exts:
    log.debug(f"adding extension {ext}")
    ext.setup(group)


def setup(dobby: "Dobby"):
    dobby.add_slave(group)
