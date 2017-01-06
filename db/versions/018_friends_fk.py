from sqlalchemy import *
from migrate import *


def upgrade(migrate_engine):
    meta = MetaData(bind=migrate_engine)

    # users = Table('users', meta, autoload=True)
    friends = Table('friends', meta, autoload=True)
    users = Table('users', meta, autoload=True)

    ForeignKeyConstraint(
        columns=[friends.c.source_user_id],
        refcolumns=[users.c.id]).create()
    ForeignKeyConstraint(
        columns=[friends.c.target_user_id],
        refcolumns=[users.c.id]).create()
    pass


def downgrade(migrate_engine):
    meta = MetaData(bind=migrate_engine)

    # users = Table('users', meta, autoload=True)
    friends = Table('friends', meta, autoload=True)
    users = Table('users', meta, autoload=True)

    ForeignKeyConstraint(
        columns=[friends.c.source_user_id],
        refcolumns=[users.c.id]).drop()
    ForeignKeyConstraint(
        columns=[friends.c.target_user_id],
        refcolumns=[users.c.id]).drop()
    pass
