from dobby import Context, Group, GroupMixin

swissvoice = Group(name="swissvoice")


@swissvoice.slave()
def zip(ctx: Context):
    pass


def setup(dobby: GroupMixin):
    dobby.add_slave(swissvoice)
