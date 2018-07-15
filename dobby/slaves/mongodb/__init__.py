from ... import Group, GroupMixin

mongodb = Group(name="mongodb")


@mongodb.slave()
def move_documents():
    pass


def setup(dobby: GroupMixin):
    dobby.add_slave(mongodb)
