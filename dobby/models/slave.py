import inspect
import logging
from inspect import Parameter
from typing import Any, Callable, Dict, Optional, Type, TypeVar, Union

from .context import Context
from .converter import CONVERTER_MAP, Converter

log = logging.getLogger(__name__)


def convert(converter, arg, **kwargs):
    origin = getattr(converter, "__origin__", False)
    if origin:
        if origin is Union:
            types = getattr(converter, "__args__")
            if isinstance(arg, types):
                return arg
            else:
                for _type in types:
                    last_exc = None
                    try:
                        return convert(_type, arg, **kwargs)
                    except Exception as e:
                        e.__cause__ = last_exc
                        last_exc = e
                        log.debug(f"Couldn't coerce {arg} to {_type}")
                    raise TypeError(f"Couldn't convert {arg} to any of {converter}") from last_exc

    if converter in CONVERTER_MAP:
        converter = CONVERTER_MAP[converter]

    if inspect.isclass(converter):
        if issubclass(converter, Converter):
            inst = converter()
            return inst.convert(arg, **kwargs)
        elif hasattr(converter, "convert") and inspect.ismethod(converter.convert):
            return converter.convert(arg, **kwargs)
    elif isinstance(converter, Converter):
        return converter.convert(arg, **kwargs)

    return converter(arg)


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
                raise Exception(f"{self} is missing self arg")

        try:
            next(iterator)
        except StopIteration:
            raise Exception(f"{self} is missing ctx arg")

        for name, param in iterator:
            if param.kind == Parameter.VAR_KEYWORD:
                kwargs.update(input_args)

            required = param.default is Parameter.empty
            if name in input_args:
                arg = input_args.pop(name)
                value = transform_param(param, arg, arguments=arguments, slave=self)
            elif required:
                raise KeyError(f"{self} requires \"{name}\" argument but it wasn't provided'")
            else:
                value = param.default
            kwargs[name] = value

        return kwargs

    def prepare(self, ctx: Context):
        ctx.slave = self
        ctx.args = [ctx] if self.instance is None else [self.instance, ctx]

    def invoke(self, ctx: Context) -> Context:
        if not self.callback:
            raise Exception(f"{self} is not a worker slave!")
        self.prepare(ctx)
        result = self.callback(*ctx.args, **ctx.kwargs)
        ctx.result = result
        return ctx


T = TypeVar("T")


def slave(name=None, cls: Type[T] = None, **kwargs) -> Callable[[Callable], T]:
    cls = cls or Slave

    def decorator(func: Callable) -> cls:
        s_name = name or func.__name__
        return cls(s_name, func, **kwargs)

    return decorator
