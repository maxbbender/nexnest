from sqlalchemy import *
from migrate import *


def downgrade(migrate_engine):
    meta = MetaData(bind=migrate_engine)

    # users = Table('users', meta, autoload=True)
    users = Table('users', meta, autoload=True)
    schools = Table('schools', meta, autoload=True)

    ForeignKeyConstraint(
        columns=[users.c.school_id],
        refcolumns=[schools.c.id]).drop()

    users.c.school_id.drop()
    pass


def upgrade(migrate_engine):
    meta = MetaData(bind=migrate_engine)

    # users = Table('users', meta, autoload=True)
    users = Table('users', meta, autoload=True)
    schools = Table('schools', meta, autoload=True)

    # password = Column("password", String(128), nullable=False)
    school_id = Column("school_id", Integer())
    school_id.create(users)

    ForeignKeyConstraint(
        columns=[users.c.school_id],
        refcolumns=[schools.c.id]).create()
    pass
