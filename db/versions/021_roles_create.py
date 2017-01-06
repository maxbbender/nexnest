from sqlalchemy import *
from migrate import *


meta = MetaData()
# Column('XXXX', String(120)),
roles = Table('roles', meta,
              Column('id', Integer(),
                     primary_key=True,
                     nullable=False),
              Column('name', String(length=128)),
              Column('description', String(length=128)),
              Column('date_created', DateTime()),
              Column('date_modified', DateTime()))


def upgrade(migrate_engine):
    meta.bind = migrate_engine
    roles.create()


def downgrade(migrate_engine):
    meta.bind = migrate_engine
    roles.drop()
