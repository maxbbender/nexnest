from sqlalchemy import *
from migrate import *


def upgrade(migrate_engine):
    meta = MetaData(bind=migrate_engine)

    # users = Table('users', meta, autoload=True)
    groupMessages = Table('group_messages', meta, autoload=True)

    # users.c.password.drop()
    groupMessages.c.date_created.drop()
    groupMessages.c.date_modified.drop()
    pass


def downgrade(migrate_engine):
    meta = MetaData(bind=migrate_engine)

    # users = Table('users', meta, autoload=True)
    groupMessages = Table('group_messages', meta, autoload=True)

    # password = Column("password", String(128), nullable=False)
    dc = Column('date_created', DateTime())
    dm = Column('date_modified', DateTime())

    # password.create(users)
    dc.create(groupMessages)
    dm.create(groupMessages)
    pass
