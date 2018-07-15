from typing import TYPE_CHECKING

from .context import Context
from .slave import Slave

if TYPE_CHECKING:
    from .task import Task


class Job:
    task: "Task"
    jobname: str
    slave: Slave

    def __init__(self, task: "Task", jobname: str, slave: Slave, **args):
        self.task = task
        self.jobname = jobname
        self.slave = slave
        self.args = args

    def __repr__(self) -> str:
        return f"<Job {self.jobid} {self.slave}>"

    @classmethod
    def load(cls, task: "Task", jobname: str, config) -> "Job":
        slave_id = config.pop("slave")
        slave = task.dobby.get_slave(slave_id)
        return cls(task, jobname, slave, **config)

    @property
    def jobid(self) -> str:
        return f"{self.task.taskid}-{self.jobname}"

    def run(self, ctx: Context):
        args = []
        kwargs = {}
        ret = self.slave.invoke(ctx, *args, **kwargs)
