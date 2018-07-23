from typing import Any, Callable, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from . import Context

DobbyBaseError = type("DobbyBaseError", (Exception,), {})


class DobbyError(DobbyBaseError):
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
        return self._format_str(self._msg)

    @property
    def hint(self) -> Optional[str]:
        if self._hint:
            return self._format_str(self._hint)

    @property
    def message(self) -> Optional[str]:
        return None


SetupError = type("SetupError", (DobbyError,), {})

EnvError = type("EnvError", (SetupError,), {})


class ConversionError(SetupError):
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
        lines = []
        if self.converter:
            lines.append(f"Converter: {self.converter}")
        if self.key:
            lines.append(f"Key: \"{self.key}\"")
        if self.value:
            lines.append(f"Provided value: {self.value}")
        return "\n".join(lines)
