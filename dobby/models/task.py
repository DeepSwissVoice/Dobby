import logging
from datetime import datetime
from operator import attrgetter
from typing import List, TYPE_CHECKING

from .calendar import Calendar
from .context import Context
from .job import Job
from ..config import DictContainer

if TYPE_CHECKING:
    from .. import Dobby

log = logging.getLogger(__name__)


class Task:
    dobby: "Dobby"
    taskid: str
    calendar: Calendar
    priority: int
    jobs: List[Job]

    def __init__(self, dobby: "Dobby", taskid: str, calendar: Calendar, priority: int = 0, jobs: List[Job] = None):
        self.dobby = dobby
        self.taskid = taskid
        self.calendar = calendar
        self.priority = priority
        self.jobs = jobs or []

        self.next_execution = None

    def __repr__(self) -> str:
        return f"<Task {self.taskid} {self.calendar}>"

    @classmethod
    def load(cls, dobby: "Dobby", taskid: str, config) -> "Task":
        calendar = Calendar.from_config(config["run"])
        inst = cls(dobby, taskid, calendar, config.get("priority", 0))

        _job = config.get("job")
        _jobs = [("main", _job)] if _job else config.get("jobs", {}).items()

        for job_name, job_config in _jobs:
            if isinstance(job_config, str):
                job_config = DictContainer(config.env, dict(slave=job_config))
            if job_config.get("enabled", True):
                inst.jobs.append(Job.load(inst, job_name, job_config))
            else:
                log.debug(f"Job {taskid}-{job_name} is disabled!")

        inst.jobs.sort(key=attrgetter("priority"), reverse=True)

        return inst

    def execute(self, ctx: Context):
        ctx.task = self
        log.info(f"{self} running {len(self.jobs)} jobs")
        for job in self.jobs:
            log.debug(f"running job {job}")
            job.run(ctx.copy())

    def execute_if_due(self, time: datetime, ctx: Context):
        if self.next_execution > time:
            return
        self.execute(ctx)
        self.plan_next_execution(time)

    def plan_next_execution(self, time: datetime):
        self.next_execution = self.calendar.next_event(time)
