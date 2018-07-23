import logging
from typing import Union

from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.database import Database
from pymongo.errors import InvalidOperation

from ... import Context, Converter, Group

log = logging.getLogger(__name__)

mongodb = Group(name="mongodb")


class DatabaseConverter(Converter):
    def convert(self, arg: Union[str, dict], **kwargs) -> Database:
        if isinstance(arg, str):
            return MongoClient(arg).get_database()
        raise NotImplementedError


def mv_documents(from_coll: Collection, to_coll: Collection, condition: dict, projection: Union[list, dict] = None, batch_size=100) -> int:
    moved_documents = 0
    count = batch_size
    while count > 0:
        documents = from_coll.find(condition, projection=projection, limit=batch_size)

        try:
            res = to_coll.insert_many(documents, ordered=False)
        except InvalidOperation:
            log.debug("no documents to move")
            return 0

        _ids = res.inserted_ids
        from_coll.delete_many({"_id": {"$in": _ids}})

        moved_documents += len(_ids)
        count = from_coll.count_documents(condition)
    return moved_documents


@mongodb.slave()
def move_documents(ctx: Context, database: DatabaseConverter, from_coll: str, to_coll: str, condition: dict,
                   projection: Union[dict, list] = None) -> int:
    database: Database
    from_coll = database[from_coll]
    to_coll = database[to_coll]
    return mv_documents(from_coll, to_coll, condition, projection)


@mongodb.slave()
def remove_documents(ctx: Context, database: DatabaseConverter, from_coll: str, condition: dict) -> int:
    database: Database
    coll = database[from_coll]
    return coll.delete_many(condition).deleted_count


def setup(dobby: Group):
    dobby.add_slave(mongodb)
