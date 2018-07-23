from typing import Any, Dict, Optional, Union

from .context import Context
from .notifications import Notification

_DEFAULT = object()


class ResultProxy:
    def __init__(self, target: Any):
        self._target = target

    def __call__(self, *args, **kwargs):
        value = self._target(*args, **kwargs)
        return ResultProxy(value)

    def __repr__(self) -> str:
        return repr(self._target)

    def __str__(self) -> str:
        return str(self._target)

    def __getattr__(self, item):
        return self.get(item)

    def __getitem__(self, item):
        return self.get(item)

    def get(self, item, default=_DEFAULT):
        try:
            value = getattr(self._target, item)
        except AttributeError:
            try:
                value = self._target[item]
            except KeyError:
                if default is _DEFAULT:
                    raise
                else:
                    value = default

        return ResultProxy(value)


DEFAULT_NOTIFICATION = Notification(text="Task {ctx.task.taskid} completed")


class Report:
    template: Notification

    def __init__(self, template: Notification):
        self.template = template

    def __call__(self, **kwargs) -> Notification:
        return self.render(**kwargs)

    @classmethod
    def load(cls, config: Optional[Union[dict, list, bool]]) -> "Report":
        if isinstance(config, dict):
            if "fields" in config or "title" in config:
                config = dict(embeds=[config])

            template = Notification(**config)
        elif isinstance(config, list):
            template = Notification(*config)
        elif config is True:
            template = DEFAULT_NOTIFICATION.copy()
        else:
            template = None

        return cls(template)

    @classmethod
    def prepare_context(cls, ctx: Context, results: Dict[str, Context]) -> Dict[str, ResultProxy]:
        kwargs = {
            "ctx": ctx
        }

        if "main" in results:
            job_ctx = results["main"]
            kwargs["ctx"] = ResultProxy(job_ctx)
            kwargs["result"] = ResultProxy(job_ctx.result)

        for key, value in results.items():
            kwargs[key] = ResultProxy(value)

        return kwargs

    def render(self, **kwargs) -> Notification:
        return self.template.format_all(**kwargs)

    def should_report(self, ctx: Context, results: Dict[str, Context]) -> bool:
        return bool(self.template)

    def create(self, ctx: Context, results: Dict[str, Context]) -> Notification:
        kwargs = self.prepare_context(ctx, results)

        return self.render(**kwargs)
