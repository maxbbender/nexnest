from sqlalchemy import *
from migrate import *


meta = MetaData()
# Column('XXXX', String(120)),
reports = Table('reports', meta,
                Column('id', Integer(),
                       primary_key=True,
                       nullable=False),
                Column('title', Text()),
                Column('content', Text()),
                Column('date_created', DateTime()),
                Column('date_modified', DateTime()))


def upgrade(migrate_engine):
    meta.bind = migrate_engine
    reports.create()
    pass


def downgrade(migrate_engine):
    meta.bind = migrate_engine
    reports.drop()
    pass
