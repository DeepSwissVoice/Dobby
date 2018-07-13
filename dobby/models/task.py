import logging
from typing import List

from .context import Context
from .job import Job
from ..config import DictContainer

log = logging.getLogger(__name__)


class Task:
    taskid: str
    jobs: List[Job]

    def __init__(self, taskid: str, jobs: List[Job] = None):
        self.taskid = taskid
        self.jobs = jobs or []

    def __repr__(self) -> str:
        return f"<Task {self.taskid}>"

    @classmethod
    def load(cls, taskid: str, config) -> "Task":
        inst = cls(taskid)

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
