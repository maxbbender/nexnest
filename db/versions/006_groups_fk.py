from sqlalchemy import *
from migrate import *


def upgrade(migrate_engine):
    meta = MetaData(bind=migrate_engine)

    # users = Table('users', meta, autoload=True)
    groups = Table('groups', meta, autoload=True)
    users = Table('users', meta, autoload=True)

    ForeignKeyConstraint(
        columns=[groups.c.leader_id],
        refcolumns=[users.c.id]).create()
    pass


def downgrade(migrate_engine):
    meta = MetaData(bind=migrate_engine)

    # users = Table('users', meta, autoload=True)
    groups = Table('groups', meta, autoload=True)
    users = Table('users', meta, autoload=True)

    ForeignKeyConstraint(
        columns=[groups.c.leader_id],
        refcolumns=[users.c.id]).drop()
    pass
