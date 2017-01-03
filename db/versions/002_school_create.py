from sqlalchemy import *
from migrate import *


meta = MetaData()
# Column('XXXX', String(120)),
schools = Table('schools', meta,
                Column('id', Integer(),
                       primary_key=True,
                       nullable=False),
                Column('name', Text()),
                Column('street', Text()),
                Column('city', Text()),
                Column('state', String(length=2)),
                Column('zip_code', String(length=5)),
                Column('phone', String(length=10)),
                Column('website', Text()),
                Column('date_created', DateTime()),
                Column('date_modified', DateTime()))


def upgrade(migrate_engine):
    meta.bind = migrate_engine
    schools.create()


def downgrade(migrate_engine):
    meta.bind = migrate_engine
    schools.drop()
