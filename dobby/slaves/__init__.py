import logging
from typing import TYPE_CHECKING

from .. import Context, Group
from ..utils import find_extensions

if TYPE_CHECKING:
    from .. import Dobby

log = logging.getLogger(__name__)

group = Group(name="dobby")


@group.slave()
def write(ctx: Context, text: str):
    log.info(text)


exts = find_extensions(__file__, __package__)
for ext in exts:
    log.debug(f"adding extension {ext}")
    ext.setup(group)


def setup(dobby: "Dobby"):
    dobby.add_slave(group)
