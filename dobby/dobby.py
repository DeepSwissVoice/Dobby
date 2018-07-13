import logging
from typing import List, TextIO

from .config import Config
from .models import Task
from .utils import setup_sentry

setup_sentry()
log = logging.getLogger(__name__)


class Dobby:
    config: Config
    tasks: List[Task]

    def __init__(self, config: Config, tasks: List[Task]):
        self.config = config
        self.tasks = tasks

    @classmethod
    def load(cls, fp: TextIO) -> "Dobby":
        config = Config.load(fp)

        tasks = []
        for taskid, task_config in config.tasks.items():
            if task_config.get("enabled", True):
                tasks.append(Task.load(taskid, task_config))
            else:
                log.debug(f"Task {taskid} disabled!")

        return cls(config, tasks)

    def run(self):
        log.info("start")
