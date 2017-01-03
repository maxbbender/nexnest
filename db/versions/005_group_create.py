from sqlalchemy import *
from migrate import *


meta = MetaData()
# Column('XXXX', String(120)),
groups = Table('groups', meta,
               Column('id', Integer(),
                      primary_key=True,
                      nullable=False),
               Column('name', Text()),
               Column('leader_id', Integer()),
               Column('date_created', DateTime()),
               Column('date_modified', DateTime()))


def upgrade(migrate_engine):
    meta.bind = migrate_engine
    groups.create()


def downgrade(migrate_engine):
    meta.bind = migrate_engine
    groups.drop()
