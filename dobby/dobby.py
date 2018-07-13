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
        for task in config.tasks.items():
            tasks.append(Task(*task))

        return cls(config, tasks)

    def run(self):
        log.info("start")
        print(self.tasks)
