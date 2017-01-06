from sqlalchemy import *
from migrate import *


def upgrade(migrate_engine):
    meta = MetaData(bind=migrate_engine)

    # users = Table('users', meta, autoload=True)
    users = Table('users', meta, autoload=True)
    roles = Table('roles', meta, autoload=True)
    user_roles = Table('user_roles', meta, autoload=True)

    ForeignKeyConstraint(
        columns=[user_roles.c.user_id],
        refcolumns=[users.c.id]).create()
    ForeignKeyConstraint(
        columns=[user_roles.c.role_id],
        refcolumns=[roles.c.id]).create()
    pass


def downgrade(migrate_engine):
    meta = MetaData(bind=migrate_engine)

# users = Table('users', meta, autoload=True)
    users = Table('users', meta, autoload=True)
    roles = Table('roles', meta, autoload=True)
    user_roles = Table('user_roles', meta, autoload=True)

    ForeignKeyConstraint(
        columns=[user_roles.c.user_id],
        refcolumns=[users.c.id]).drop()
    ForeignKeyConstraint(
        columns=[user_roles.c.role_id],
        refcolumns=[roles.c.id]).drop()
    pass
