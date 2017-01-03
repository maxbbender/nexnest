from sqlalchemy import *
from migrate import *


def upgrade(migrate_engine):
    meta = MetaData(bind=migrate_engine)

    # users = Table('users', meta, autoload=True)
    landlords = Table('landlords', meta, autoload=True)
    listings = Table('listings', meta, autoload=True)
    landlord_listings = Table('landlord_listings', meta, autoload=True)

    ForeignKeyConstraint(
        columns=[landlord_listings.c.landlord_id],
        refcolumns=[landlords.c.user_id]).create()
    ForeignKeyConstraint(
        columns=[landlord_listings.c.listing_id],
        refcolumns=[listings.c.id]).create()
    pass


def downgrade(migrate_engine):
    meta = MetaData(bind=migrate_engine)

    # users = Table('users', meta, autoload=True)
    landlords = Table('landlords', meta, autoload=True)
    listings = Table('listings', meta, autoload=True)
    landlord_listings = Table('landlord_listings', meta, autoload=True)

    ForeignKeyConstraint(
        columns=[landlord_listings.c.landlord_id],
        refcolumns=[landlords.c.user_id]).drop()
    ForeignKeyConstraint(
        columns=[landlord_listings.c.listing_id],
        refcolumns=[listings.c.id]).drop()
    pass
