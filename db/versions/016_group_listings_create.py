from sqlalchemy import *
from migrate import *


meta = MetaData()
# Column('XXXX', String(120)),
group_listings = Table('group_listings', meta,
                       Column('id', Integer(), primary_key=True, nullable=False),
                       Column('group_id', Integer(),
                              nullable=False),
                       Column('listing_id', Integer(),
                              nullable=False))


def upgrade(migrate_engine):
    meta.bind = migrate_engine
    group_listings.create()


def downgrade(migrate_engine):
    meta.bind = migrate_engine
    group_listings.drop()
