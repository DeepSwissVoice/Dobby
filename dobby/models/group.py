import abc
import importlib
import inspect
import types
from typing import Callable, Dict, Iterator, List, Union

from .slave import Slave, slave as slave_decorator


class GroupMixin(abc.ABC):
    slaves: Dict[str, Slave]

    def __init__(self, **kwargs):
        self.slaves = {}
        super().__init__(**kwargs)

    def add_slave(self, slave: Slave):
        key = slave.name
        if key in self.slaves:
            raise KeyError(f"{self} already has a Slave \"{key}\"")

        if isinstance(self, Slave):
            slave.parent = self

        self.slaves[key] = slave

    def add_ext(self, ext):
        members = inspect.getmembers(ext)
        for name, member in members:
            if isinstance(member, Slave):
                if member.parent is None:
                    self.add_slave(member)
                continue

    def load_ext(self, ext: str):
        ext = importlib.import_module(ext)
        if hasattr(ext, "setup"):
            ext.setup(self)
        elif isinstance(ext, Slave):
            self.add_slave(ext)
        elif isinstance(ext, types.ModuleType):
            raise Exception(f"{ext} is a module without a setup function!")

    def get_slave(self, key: Union[str, List[str]]) -> Slave:
        if isinstance(key, str):
            key = key.split(".")

        if not key:
            if isinstance(self, Slave):
                return self
            else:
                raise KeyError(f"key lead to {type(self)} instead of a Slave")

        prim, *key = key
        slave = self.slaves[prim]
        if isinstance(slave, GroupMixin):
            return slave.get_slave(key)
        return slave

    def walk_slaves(self) -> Iterator[Slave]:
        for slave in self.slaves.values():
            if isinstance(slave, GroupMixin):
                yield from slave.walk_slaves()
            else:
                yield slave

    def slave(self, *args, **kwargs) -> Callable[[Callable], Slave]:
        def decorator(func: Callable) -> Slave:
            slave = slave_decorator(*args, **kwargs)(func)
            self.add_slave(slave)
            return slave

        return decorator

    def group(self, *args, **kwargs) -> Callable[[Callable], "Group"]:
        def decorator(func: Callable) -> Group:
            slave = group(*args, **kwargs)(func)
            self.add_slave(slave)
            return slave

        return decorator


class Group(GroupMixin, Slave):
    pass


def group(name=None, **kwargs) -> Callable[[Callable], Group]:
    return slave_decorator(name, cls=Group, **kwargs)
