from sqlalchemy import *
from migrate import *


def upgrade(migrate_engine):
    meta = MetaData(bind=migrate_engine)

    # users = Table('users', meta, autoload=True)
    group = Table('groups', meta, autoload=True)

    # password = Column("password", String(128), nullable=False)
    active = Column("active", Boolean, nullable=True)

    # password.create(users)
    active.create(group)
    pass


def downgrade(migrate_engine):
    meta = MetaData(bind=migrate_engine)

    group = Table('groups', meta, autoload=True)

    # users.c.password.drop()
    group.c.active.drop()
    pass
