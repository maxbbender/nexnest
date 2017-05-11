from sqlalchemy import *
from migrate import *


meta = MetaData()
# Column('XXXX', String(120)),
landlords = Table('landlords', meta,
                  Column('user_id', Integer(),
                         primary_key=True,
                         nullable=False),
                  Column('online_pay', Boolean()),
                  Column('check_pay', Boolean()),
                  Column('street', Text()),
                  Column('city', Text()),
                  Column('state', String(length=2)),
                  Column('zip_code', String(length=5)),
                  Column('phone', Text()),
                  Column('dob', Date()))


def upgrade(migrate_engine):
    meta.bind = migrate_engine
    landlords.create()


def downgrade(migrate_engine):
    meta.bind = migrate_engine
    landlords.drop()
