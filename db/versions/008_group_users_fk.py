from sqlalchemy import *
from migrate import *


def upgrade(migrate_engine):
    meta = MetaData(bind=migrate_engine)

    # users = Table('users', meta, autoload=True)
    groups = Table('groups', meta, autoload=True)
    users = Table('users', meta, autoload=True)
    group_users = Table('group_users', meta, autoload=True)

    ForeignKeyConstraint(
        columns=[group_users.c.group_id],
        refcolumns=[groups.c.id]).create()
    ForeignKeyConstraint(
        columns=[group_users.c.user_id],
        refcolumns=[users.c.id]).create()

    pass


def downgrade(migrate_engine):
    meta = MetaData(bind=migrate_engine)

    # users = Table('users', meta, autoload=True)
    groups = Table('groups', meta, autoload=True)
    users = Table('users', meta, autoload=True)
    group_users = Table('group_users', meta, autoload=True)

    ForeignKeyConstraint(
        columns=[group_users.c.group_id],
        refcolumns=[groups.c.id]).drop()
    ForeignKeyConstraint(
        columns=[group_users.c.user_id],
        refcolumns=[users.c.id]).drop()
    pass
