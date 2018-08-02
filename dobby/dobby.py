import logging
import time
from datetime import datetime
from operator import attrgetter
from pathlib import Path
from typing import Dict, List, Union

from . import __version__, slaves
from .config import Config
from .models import Context, GroupMixin, Task
from .models.notifications import Notification, NotificationManager
from .utils import human_timedelta, setup_sentry

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

    def send_notification(self, notification: Union[Notification, Dict] = None, *embeds, **kwargs):
        if not isinstance(notification, Notification):
            notification = Notification(notification, *embeds, **kwargs)
        return self.notification_manager.send(notification)

    def wait_for_next(self):
        now = datetime.now()
        next_time = min(task.next_execution for task in self.tasks)
        sleep_time = (next_time - now).total_seconds()
        if sleep_time >= 0:
            log.info(f"sleeping for {human_timedelta(sleep_time)}")
            time.sleep(sleep_time)
        else:
            log.warning(f"{human_timedelta(-sleep_time)} behind schedule!")

    def execute_due_tasks(self):
        for task in self.tasks:
            task.execute_if_due(datetime.now(), self.ctx.copy())

    def run(self):
        log.info("start")

        self.send_notification(dict(
            title="Dobby is starting",
            fields=[dict(title="Tasks",
                         value=len(self.tasks)),
                    dict(title="Jobs",
                         value=sum(len(task.jobs) for task in self.tasks))],
            footer=f"Dobby v{__version__}"
        ))

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
