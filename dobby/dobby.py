import logging
import time
from datetime import datetime
from pathlib import Path
from typing import List

from . import slaves
from .config import Config
from .models import GroupMixin, Task
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
        config = Config.load(fp)

        inst = cls(config)

        for ext in config.ext:
            inst.load_ext(ext)

        for taskid, task_config in config.tasks.items():
            if task_config.get("enabled", True):
                inst.tasks.append(Task.load(inst, taskid, task_config))
            else:
                log.debug(f"Task {taskid} disabled!")

        return inst

    def run(self):
        log.info("start")
        print(self.tasks, flush=True)
        print([task.jobs for task in self.tasks], flush=True)
        while True:
            now = datetime.now()
            next_time = min(task.next_execution(now) for task in self.tasks)
            print(next_time, flush=True)
            sleep_time = (next_time - now).total_seconds()
            log.debug(f"sleeping for {sleep_time} second(s)")
            time.sleep(sleep_time)
            break
