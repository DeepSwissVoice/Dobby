import abc
import inspect
import logging
from typing import Any, Union

from ..config import DictContainer, ListContainer
from ..errors import ConversionError

log = logging.getLogger(__name__)


class Converter(abc.ABC):
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


class DictConverter(Converter):
    def convert(self, arg: Any, **kwargs) -> dict:
        if isinstance(arg, DictContainer):
            return arg.to_normal()
        return dict(arg)


class ListConverter(Converter):
    def convert(self, arg: Any, **kwargs) -> list:
        if isinstance(arg, ListContainer):
            return arg.to_normal()
        return list(arg)


CONVERTER_MAP = {
    dict: DictConverter,
    list: ListConverter
}


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
                    except ConversionError:
                        raise
                    except Exception as e:
                        e.__cause__ = last_exc
                        last_exc = e
                        log.debug(f"Couldn't coerce {arg!r} to {_type}")
                    raise ConversionError(f"Couldn't convert {arg!r} to any of {converter}", value=arg, converter=converter) from last_exc

    if converter in CONVERTER_MAP:
        converter = CONVERTER_MAP[converter]

    try:
        if inspect.isclass(converter):
            if issubclass(converter, Converter):
                inst = converter()
                return inst.convert(arg, **kwargs)
            elif hasattr(converter, "convert") and inspect.ismethod(converter.convert):
                return converter.convert(arg, **kwargs)
        elif isinstance(converter, Converter):
            return converter.convert(arg, **kwargs)

        return converter(arg)
    except ConversionError:
        raise
    except Exception as e:
        raise ConversionError(f"Couldn't convert {arg!r} using {converter}", value=arg, converter=converter,
                              hint="Make sure that you're passing a valid value for the parameter \"{self.key}\"") from e
