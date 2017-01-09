from sqlalchemy import *
from migrate import *


def downgrade(migrate_engine):
    meta = MetaData(bind=migrate_engine)

    # users = Table('users', meta, autoload=True)
    group_users = Table('group_users', meta, autoload=True)

    # users.c.password.drop()
    group_users.c.accepted.drop()
    group_users.c.show.drop()
    pass


def upgrade(migrate_engine):
    meta = MetaData(bind=migrate_engine)

    # users = Table('users', meta, autoload=True)
    group_users = Table('group_users', meta, autoload=True)

    # password = Column("password", String(128), nullable=False)
    accepted = Column("accepted", Boolean())
    show = Column("show", Boolean())

    # password.create(users)
    accepted.create(group_users)
    show.create(group_users)
    pass
