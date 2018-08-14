from typing import Any, Callable, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from . import Context

DobbyBaseError = type("DobbyBaseError", (Exception,), {})

DobbyBaseError.__doc__ = """This exception is just a subclass of `Exception`.

It doesn't add any extra functionality but it's supposed to be the only error ever
raised by Dobby.
"""


class DobbyError(DobbyBaseError):
    """
    A base class for all Dobby-related errors that provide a bit more info.
    A `DobbyError` can help you fix the problem by giving a (useless) hint and the `Context`
    in which the error was raised.

    Attributes:
        ctx: `Context` that was passed to the error (optional)
    """

    _msg: str
    _hint: Optional[str]
    ctx: Optional["Context"]

    def __init__(self, msg: str, **kwargs):
        self._msg = msg
        self._hint = kwargs.pop("hint", None)
        self.ctx = kwargs.pop("ctx", None)
        super().__init__(**kwargs)

    def __repr__(self) -> str:
        return f"{type(self).__name__}({self.msg!r})"

    def __str__(self) -> str:
        lines = [self.msg]
        if self.message:
            lines.append(f"=== Message ===\n{self.message}")
        if self.ctx:
            lines.append(f"=== Context ===\n{self.ctx.prettify()}")
        if self.hint:
            lines.append(f"===  Hint   ===\n{self.hint}")

        return "\n\n".join(lines)

    def _format_str(self, s: str) -> str:
        return s.format(msg=self._msg, hint=self._hint, ctx=self.ctx, self=self)

    @property
    def msg(self) -> str:
        """Formatted message that was passed to the error."""
        return self._format_str(self._msg)

    @property
    def hint(self) -> Optional[str]:
        """The hint which may have been provided when creating the error."""
        if self._hint:
            return self._format_str(self._hint)

    @property
    def message(self) -> Optional[str]:
        """A property for subclasses to override.
        For `DobbyError` this will always be `None`.

        If the message is a truthy value then it'll be included in the string representation
        of the error.
        """
        return None


SetupError = type("SetupError", (DobbyError,), {})

SetupError.__doc__ = """
A subclass of `DobbyError` which really doesn't add anything to the base class **but**
it is (or at least should be) the base class for all errors that happen during the setup of
Dobby (that's basically everything before going to sleep to wait for the first task).
"""

EnvError = type("EnvError", (SetupError,), {})

EnvError.__doc__ = """
Finally we get to the first *real* error which is raised when trying to access a key from
the `env` that isn't defined in the environment variables or the `env` config key.
"""


class ConversionError(SetupError):
    """Raised when the conversion of a config value to the designated slave argument type fails.

    Attributes:
        key: Name of the parameter that the `value` was supposed to be converted for
        value: Value that was passed to the `Converter` to be converted
        converter: `Converter` that tried to convert the `value`
    """

    key: str
    value: Any
    converter: Callable

    def __init__(self, msg: str, **kwargs):
        self.key = kwargs.pop("key", None)
        self.value = kwargs.pop("value", None)
        self.converter = kwargs.pop("converter")
        super().__init__(msg, **kwargs)

    @property
    def message(self) -> str:
        """
        A string which provides information on which `Converter` was used,
        what was to be converted and for which slave argument.
        """
        lines = []
        if self.converter:
            lines.append(f"Converter: {self.converter}")
        if self.key:
            lines.append(f"Key: \"{self.key}\"")
        if self.value:
            lines.append(f"Provided value: {self.value}")
        return "\n".join(lines)
