import copy
from typing import Any, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from .job import Job
    from .slave import Slave
    from .task import Task
    from ..dobby import Dobby


class Context:
    dobby: "Dobby"
    task: "Task"
    job: "Job"
    slave: "Slave"
    input_args: dict
    args: list
    kwargs: dict
    result: Any
    exception: Optional[Exception]

    def __init__(self, dobby: "Dobby", **kwargs):
        self.dobby = dobby
        self.task = kwargs.pop("task", None)
        self.job = kwargs.pop("job", None)
        self.slave = kwargs.pop("slave", None)
        self.input_args = kwargs.pop("input_args", None)
        self.args = kwargs.pop("args", None)
        self.kwargs = kwargs.pop("kwargs", None)
        self.result = kwargs.pop("result", None)
        self.exception = kwargs.pop("exception", None)

    def __str__(self) -> str:
        return "Context!"

    def copy(self) -> "Context":
        return copy.copy(self)
