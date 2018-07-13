from typing import Callable

from .context import Context


class Slave:
    def __init__(self, callback: Callable):
        self.callback = callback

    def invoke(self, ctx: Context):
        self.callback(ctx, *ctx.args, **ctx.kwargs)


def slave(func: Callable) -> Slave:
    return Slave(func)
