from sqlalchemy import *
from migrate import *


def upgrade(migrate_engine):
    meta = MetaData(bind=migrate_engine)

    # users = Table('users', meta, autoload=True)
    messages = Table('messages', meta, autoload=True)
    users = Table('users', meta, autoload=True)

    ForeignKeyConstraint(
        columns=[messages.c.user_id],
        refcolumns=[users.c.id]).create()
    pass


def downgrade(migrate_engine):
    meta = MetaData(bind=migrate_engine)

    # users = Table('users', meta, autoload=True)
    messages = Table('messages', meta, autoload=True)
    users = Table('users', meta, autoload=True)

    ForeignKeyConstraint(
        columns=[messages.c.user_id],
        refcolumns=[users.c.id]).drop()
    pass
