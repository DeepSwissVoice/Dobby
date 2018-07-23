import inspect
import logging
from inspect import Parameter
from typing import Any, Callable, Dict, Optional, Type, TypeVar

from .context import Context
from .converter import convert
from ..errors import ConversionError, SetupError

log = logging.getLogger(__name__)


def transform_param(param: Parameter, arg: Any, **kwargs) -> Any:
    converter = param.annotation
    if converter is Parameter.empty:
        return arg

    return convert(converter, arg, **kwargs)


class Slave:
    name: str
    callback: Optional[Callable]
    instance: Optional[Any]
    parent: Optional["Slave"]
    params: Dict[str, Parameter]

    def __init__(self, name: str, callback: Callable = None, **kwargs):
        self.name = name
        self.callback = callback

        self.instance = None
        self.parent = kwargs.get("parent")

        if callback:
            signature = inspect.signature(callback)
            self.params = signature.parameters.copy()
        else:
            self.params = None

    def __repr__(self) -> str:
        return f"<Slave {self.qualified_name}>"

    def __get__(self, instance, owner):
        if instance is not None:
            self.instance = instance
        return self

    @property
    def qualified_name(self) -> str:
        if isinstance(self.parent, Slave):
            return self.parent.qualified_name + "." + self.name
        return self.name

    def transform_arguments(self, arguments: dict) -> dict:
        kwargs = {}
        input_args = arguments.copy()
        iterator = iter(self.params.items())

        if self.instance is not None:
            try:
                next(iterator)
            except StopIteration:
                raise SyntaxError(f"{self} is bound to an instance but missing the self arg."
                                  "If you're the maintainer of this slave, please make sure to add \"self\" as the first positional argument")

        try:
            next(iterator)
        except StopIteration:
            raise SyntaxError(f"{self} is missing ctx arg. All slaves must accept the context as a positional argument."
                              "If you're the maintainer of this slave, please add it!")

        for name, param in iterator:
            if param.kind == Parameter.VAR_KEYWORD:
                kwargs.update(input_args)

            required = param.default is Parameter.empty
            if name in input_args:
                arg = input_args.pop(name)
                try:
                    value = transform_param(param, arg, arguments=arguments, slave=self)
                except ConversionError as e:
                    e.key = name
                    raise e

            elif required:
                raise SetupError(f"{self} requires \"{name}\" argument but it wasn't provided",
                                 hint="Make sure to pass all required arguments to the slave in your config file!")
            else:
                value = param.default
            kwargs[name] = value

        return kwargs

    def prepare(self, ctx: Context):
        ctx.slave = self
        ctx.args = [ctx] if self.instance is None else [self.instance, ctx]

    def invoke(self, ctx: Context):
        if not self.callback:
            raise SetupError(f"{self} is not a worker slave but a group!", ctx=ctx, hint="Check whether you've entered the slave key correctly!")

        self.prepare(ctx)
        try:
            result = self.callback(*ctx.args, **ctx.kwargs)
            ctx.result = result
        except Exception as e:
            ctx.exception = e


T = TypeVar("T")


def slave(name=None, cls: Type[T] = None, **kwargs) -> Callable[[Callable], T]:
    cls = cls or Slave

    def decorator(func: Callable) -> cls:
        s_name = name or func.__name__
        return cls(s_name, func, **kwargs)

    return decorator
