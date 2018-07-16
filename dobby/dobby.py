import logging
import time
from datetime import datetime
from pathlib import Path
from typing import List

from . import slaves
from .config import Config
from .models import Context, GroupMixin, Task
from .utils import setup_sentry

setup_sentry()
log = logging.getLogger(__name__)


class Dobby(GroupMixin):
    config: Config
    tasks: List[Task]

    def __init__(self, config: Config, tasks: List[Task] = None):
        super().__init__()

        self.config = config
        self.tasks = tasks or []
        slaves.setup(self)

    @classmethod
    def load(cls, fp: Path) -> "Dobby":
        log.debug("loading config")
        config = Config.load(fp)

        inst = cls(config)

        log.debug("loading extensions")
        for ext in config.ext:
            inst.load_ext(ext)

        log.debug("building tasks")
        for taskid, task_config in config.tasks.items():
            if task_config.get("enabled", True):
                inst.tasks.append(Task.load(inst, taskid, task_config))
            else:
                log.debug(f"Task {taskid} disabled!")

        return inst

    def wait_for_next(self) -> Task:
        now = datetime.now()
        next_time, next_task = min((task.next_execution(now), task) for task in self.tasks)
        sleep_time = (next_time - now).total_seconds()
        log.debug(f"sleeping for {sleep_time} second(s)")
        time.sleep(sleep_time)
        return next_task

    def run(self):
        log.info("start")
        while True:
            task = self.wait_for_next()
            ctx = Context(self)
            task.execute(ctx.copy())
            log.debug("loop finished")
