from sqlalchemy import *
from migrate import *


meta = MetaData()
reports = Table('reports', meta,
                Column('id', Integer(),
                       primary_key=True,
                       nullable=False),
                Column('title', Text()),
                Column('content', Text()),
                Column('type', String(50)),
                Column('user_id', Integer()),
                Column('source_url', Text()),
                Column('date_created', DateTime()),
                Column('date_modified', DateTime()))


def upgrade(migrate_engine):
    meta.bind = migrate_engine
    reports.create()

    # Foreign Keys
    users = Table('users', meta, autoload=True)
    ForeignKeyConstraint(
        columns=[reports.c.user_id],
        refcolumns=[users.c.id]).create()
    pass


def downgrade(migrate_engine):
    meta.bind = migrate_engine

    # Foreign Keys
    users = Table('users', meta, autoload=True)
    ForeignKeyConstraint(
        columns=[reports.c.user_id],
        refcolumns=[users.c.id]).drop()
    reports.drop()
    pass
