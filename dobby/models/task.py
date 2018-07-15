import logging
from datetime import datetime
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
    jobs: List[Job]

    def __init__(self, dobby: "Dobby", taskid: str, calendar: Calendar, jobs: List[Job] = None):
        self.dobby = dobby
        self.taskid = taskid
        self.calendar = calendar
        self.jobs = jobs or []

    def __repr__(self) -> str:
        return f"<Task {self.taskid} {self.calendar}>"

    @classmethod
    def load(cls, dobby: "Dobby", taskid: str, config) -> "Task":
        calendar = Calendar.from_config(config["run"])
        inst = cls(dobby, taskid, calendar)

        _job = config.get("job")
        _jobs = [("main", _job)] if _job else config.get("jobs", {}).items()

        for job_name, job_config in _jobs:
            if isinstance(job_config, str):
                job_config = DictContainer(config.env, dict(slave=job_config))
            if job_config.get("enabled", True):
                inst.jobs.append(Job.load(inst, job_name, job_config))
            else:
                log.debug(f"Job {taskid}-{job_name} is disabled!")
        return inst

    def execute(self, ctx: Context):
        log.info(f"{self} running {len(self.jobs)} jobs")
        for job in self.jobs:
            job.run(ctx)

    def next_execution(self, time: datetime) -> datetime:
        return self.calendar.next_event(time)
