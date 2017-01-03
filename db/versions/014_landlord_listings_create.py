from sqlalchemy import *
from migrate import *


meta = MetaData()
# Column('XXXX', String(120)),
landlord_listings = Table('landlord_listings', meta,
                          Column('landlord_id', Integer(),
                                 primary_key=True,
                                 nullable=False),
                          Column('listing_id', Integer(),
                                 primary_key=True,
                                 nullable=False))


def upgrade(migrate_engine):
    meta.bind = migrate_engine
    landlord_listings.create()


def downgrade(migrate_engine):
    meta.bind = migrate_engine
    landlord_listings.drop()
