from dobby import Group, GroupMixin

swissvoice = Group(name="swissvoice")


@swissvoice.slave()
def zip():
    pass


def setup(dobby: GroupMixin):
    dobby.add_slave(swissvoice)
