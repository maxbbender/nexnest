from sqlalchemy import *
from migrate import *


def upgrade(migrate_engine):
    meta = MetaData(bind=migrate_engine)

    # users = Table('users', meta, autoload=True)
    maintenances = Table('maintenances', meta, autoload=True)
    users = Table('users', meta, autoload=True)

    user_id = Column('user_id', Integer())

    user_id.create(maintenances)

    ForeignKeyConstraint(
        columns=[maintenances.c.user_id],
        refcolumns=[users.c.id]).create()
    pass


def downgrade(migrate_engine):
    meta = MetaData(bind=migrate_engine)

    # users = Table('users', meta, autoload=True)
    maintenances = Table('maintenances', meta, autoload=True)
    users = Table('users', meta, autoload=True)

    ForeignKeyConstraint(
        columns=[maintenances.c.user_id],
        refcolumns=[users.c.id]).drop()

    maintenances.c.user_id.drop()
    pass
