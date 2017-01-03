from sqlalchemy import *
from migrate import *


meta = MetaData()
# Column('XXXX', String(120)),
listing_favorites = Table('listing_favorites', meta,
                          Column('listing_id', Integer(),
                                 primary_key=True,
                                 nullable=False),
                          Column('user_id', Integer(),
                                 primary_key=True,
                                 nullable=False))


def upgrade(migrate_engine):
    meta.bind = migrate_engine
    listing_favorites.create()


def downgrade(migrate_engine):
    meta.bind = migrate_engine
    listing_favorites.drop()
