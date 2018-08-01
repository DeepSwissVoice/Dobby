import abc
import importlib
import inspect
import logging
from typing import Any, Callable, Mapping, Type, Union

from ..errors import ConversionError

log = logging.getLogger(__name__)

CONVERTER_MAP = {}


class Converter(abc.ABC):
    options: Mapping

    def __init__(self, **kwargs):
        self.options = kwargs

    def __repr__(self) -> str:
        sig = inspect.signature(self.convert)
        return_hint = sig.return_annotation
        if return_hint not in {sig.empty, Any}:
            return_name = return_hint.__name__ if inspect.isclass(return_hint) else return_hint
            return f"[ str -> {return_name} ]"
        else:
            return f"<{type(self).__name__}>"

    @abc.abstractmethod
    def convert(self, arg: Any, **kwargs) -> Any:
        pass


class FuncConverter(Converter):
    def __init__(self, func: Callable, **kwargs):
        self.func = func
        func_sig = inspect.signature(func)

        self.convert.__annotations__.update({
            "arg": func_sig.parameters["arg"].annotation,
            "return": func_sig.return_annotation
        })

        super().__init__(**kwargs)

    def convert(self, arg: Any, **kwargs) -> Any:
        return self.func(arg, **kwargs)


def _class_converter(cls: Type[Converter], *targets: Any, **kwargs) -> Converter:
    conv = cls(**kwargs)
    return conv


def _func_converter(func: Callable, *targets: Any, **kwargs) -> Converter:
    conv = FuncConverter(func, **kwargs)
    return conv


def converter(*targets: Any, **kwargs):
    for target in targets:
        if not inspect.isclass(target):
            raise TypeError(f"targets must be a tuple of types, not {target}")

    def decorator(arg):
        if inspect.isclass(arg) and issubclass(arg, Converter):
            _converter = _class_converter(arg, *targets, **kwargs)
        else:
            _converter = _func_converter(arg, *targets, **kwargs)

        for target in targets:
            if target in CONVERTER_MAP:
                raise KeyError(f"There's already a converter for {target}")
            CONVERTER_MAP[target] = _converter

        return _converter

    return decorator


def convert(_converter, arg, **kwargs):
    origin = getattr(_converter, "__origin__", False)
    if origin:
        if origin is Union:
            types = getattr(_converter, "__args__")
            if isinstance(arg, types):
                return arg
            else:
                for _type in types:
                    last_exc = None
                    try:
                        return convert(_type, arg, **kwargs)
                    except ConversionError:
                        raise
                    except Exception as e:
                        e.__cause__ = last_exc
                        last_exc = e
                        log.debug(f"Couldn't coerce {arg!r} to {_type}")
                    raise ConversionError(f"Couldn't convert {arg!r} to any of {_converter}", value=arg, converter=_converter) from last_exc

    if _converter in CONVERTER_MAP:
        _converter = CONVERTER_MAP[_converter]

    try:
        if inspect.isclass(_converter):
            if issubclass(_converter, Converter):
                inst = _converter()
                return inst.convert(arg, **kwargs)
            elif hasattr(_converter, "convert") and inspect.ismethod(_converter.convert):
                return _converter.convert(arg, **kwargs)
        elif isinstance(_converter, Converter):
            return _converter.convert(arg, **kwargs)

        return _converter(arg)
    except ConversionError:
        raise
    except Exception as e:
        raise ConversionError(f"Couldn't convert {arg!r} using {_converter}", value=arg, converter=_converter,
                              hint="Make sure that you're passing a valid value for the parameter \"{self.key}\"") from e


importlib.import_module("._builtin_converters", __package__)
