from typing import Callable, Optional, Type, TypeVar

from .context import Context


class Slave:
    name: str
    callback: Optional[Callable]
    parent: Optional["Slave"]

    def __init__(self, name: str, callback: Callable = None, **kwargs):
        self.name = name
        self.callback = callback

        self.parent = kwargs.get("parent")

    def __repr__(self) -> str:
        return f"<Slave {self.qualified_name}>"

    @property
    def qualified_name(self) -> str:
        if isinstance(self.parent, Slave):
            return self.parent.qualified_name + "." + self.name
        return self.name

    def invoke(self, ctx: Context):
        if self.callback:
            self.callback(ctx, *ctx.args, **ctx.kwargs)
        else:
            raise Exception(f"{self} is not a worker slave!")


T = TypeVar("T")


def slave(name=None, cls: Type[T] = None, **kwargs) -> Callable[[Callable], T]:
    cls = cls or Slave

    def decorator(func: Callable) -> cls:
        s_name = name or func.__name__
        return cls(s_name, func, **kwargs)

    return decorator
