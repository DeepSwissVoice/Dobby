import logging
from typing import TYPE_CHECKING

from .context import Context
from .slave import Slave

if TYPE_CHECKING:
    from .task import Task

log = logging.getLogger(__name__)


class Job:
    task: "Task"
    jobname: str
    slave: Slave
    raw_kwargs: dict
    kwargs: dict

    def __init__(self, task: "Task", jobname: str, slave: Slave, **kwargs):
        self.task = task
        self.jobname = jobname
        self.slave = slave
        self.raw_kwargs = kwargs
        self.kwargs = {}

        self.prepare()

    def __repr__(self) -> str:
        return f"<Job {self.jobid} >>{self.slave.qualified_name}>"

    @classmethod
    def load(cls, task: "Task", jobname: str, config) -> "Job":
        slave_id = config.pop("slave")
        slave = task.dobby.get_slave(slave_id)
        return cls(task, jobname, slave, **config)

    @property
    def jobid(self) -> str:
        return f"{self.task.taskid}-{self.jobname}"

    def prepare(self):
        log.debug(f"{self} preparing")
        self.kwargs = self.slave.transform_arguments(self.raw_kwargs)

    def run(self, ctx: Context):
        ctx.job = self
        ctx.input_args = self.raw_kwargs
        ctx.kwargs = self.kwargs
        ctx = self.slave.invoke(ctx)
        log.info(f"{self} returned {ctx.result}")
