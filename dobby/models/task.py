import logging
from typing import Any, Dict, List

from .job import Job

log = logging.getLogger(__name__)


class Task:
    taskid: str
    jobs: List[Job]

    def __init__(self, taskid: str, jobs: List[Job] = None):
        self.taskid = taskid
        self.jobs = jobs or []

    def __str__(self) -> str:
        return f"<Task {self.taskid}>"

    @classmethod
    def load(cls, taskid: str, config: Dict[str, Any]) -> "Task":
        return cls(taskid)

    def execute(self):
        log.info(f"{self} running {len(self.jobs)} jobs")
        for job in self.jobs:
            job.run()
