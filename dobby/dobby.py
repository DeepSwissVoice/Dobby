import logging
import time
from datetime import datetime
from operator import attrgetter
from pathlib import Path
from typing import List

from . import slaves
from .config import Config
from .models import Context, GroupMixin, Task
from .models.notifications import NotificationManager
from .utils import setup_sentry

setup_sentry()
log = logging.getLogger(__name__)


class Dobby(GroupMixin):
    config: Config
    notification_manager: NotificationManager
    tasks: List[Task]
    ctx: Context

    def __init__(self, config: Config, tasks: List[Task] = None):
        super().__init__()

        self.config = config
        self.notification_manager = NotificationManager.load(config.notifications)
        self.tasks = tasks or []
        self.ctx = Context(self)
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

        inst.tasks.sort(key=attrgetter("priority"), reverse=True)

        return inst

    def wait_for_next(self):
        now = datetime.now()
        next_time = min(task.next_execution for task in self.tasks)
        sleep_time = (next_time - now).total_seconds()
        if sleep_time >= 0:
            log.debug(f"sleeping for {sleep_time} second(s)")
            time.sleep(sleep_time)
        else:
            log.warning(f"{-sleep_time}s behind schedule!")

    def execute_due_tasks(self):
        for task in self.tasks:
            task.execute_if_due(datetime.now(), self.ctx.copy())

    def run(self):
        log.info("start")
        now = datetime.now()
        for task in self.tasks:
            task.plan_next_execution(now)

        while True:
            self.wait_for_next()
            self.execute_due_tasks()
            log.debug("loop finished")

    def test(self):
        log.info("executing all tasks!")
        for task in self.tasks:
            task.execute(self.ctx.copy())
        log.info("done")
