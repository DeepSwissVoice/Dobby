from typing import Union

from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.database import Database

from ... import Context, Converter, Group

mongodb = Group(name="mongodb")


class DatabaseConverter(Converter):
    def convert(self, arg: Union[str, dict], **kwargs) -> Database:
        if isinstance(arg, str):
            return MongoClient(arg).get_database()
        raise NotImplementedError("Not yet implemented")


def mv_documents(from_coll: Collection, to_coll: Collection, condition: dict, batch_size=100) -> int:
    moved_documents = 0
    count = batch_size
    while count > 0:
        documents = from_coll.find(condition, limit=batch_size)
        res = to_coll.insert_many(documents, ordered=False)
        _ids = res.inserted_ids
        from_coll.delete_many({"_id": {"$in": _ids}})

        moved_documents += len(_ids)
        count = from_coll.count_documents(condition)
    return move_documents


@mongodb.slave()
def move_documents(ctx: Context, database: DatabaseConverter, from_coll: str, to_coll: str, condition: dict) -> int:
    database: Database
    from_coll = database[from_coll]
    to_coll = database[to_coll]
    return mv_documents(from_coll, to_coll, condition)


@mongodb.slave()
def remove_documents(ctx: Context, database: DatabaseConverter, from_coll: str, condition: dict) -> int:
    database: Database
    coll = database[from_coll]
    return coll.delete_many(condition).deleted_count


def setup(dobby: Group):
    dobby.add_slave(mongodb)
