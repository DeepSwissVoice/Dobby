from typing import List, TextIO

from .models import Task


class Dobby:
    tasks: List[Task]

    def __init__(self):
        pass

    @classmethod
    def load(cls, fp: TextIO) -> "Dobby":
        return cls()

    def run(self):
        pass
