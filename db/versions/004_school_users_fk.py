from sqlalchemy import *
from migrate import *


def upgrade(migrate_engine):
    meta = MetaData(bind=migrate_engine)

    # users = Table('users', meta, autoload=True)
    school_users = Table('school_users', meta, autoload=True)
    schools = Table('schools', meta, autoload=True)
    users = Table('users', meta, autoload=True)

    ForeignKeyConstraint(
        columns=[school_users.c.user_id],
        refcolumns=[users.c.id]).create()

    ForeignKeyConstraint(
        columns=[school_users.c.school_id],
        refcolumns=[schools.c.id]).create()
    pass


def downgrade(migrate_engine):
    meta = MetaData(bind=migrate_engine)

    # users = Table('users', meta, autoload=True)
    school_users = Table('school_users', meta, autoload=True)
    schools = Table('schools', meta, autoload=True)
    users = Table('users', meta, autoload=True)

    ForeignKeyConstraint(
        columns=[school_users.c.user_id],
        refcolumns=[users.c.id]).drop()

    ForeignKeyConstraint(
        columns=[school_users.c.school_id],
        refcolumns=[schools.c.id]).drop()
    pass
