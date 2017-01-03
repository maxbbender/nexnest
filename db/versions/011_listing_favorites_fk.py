from sqlalchemy import *
from migrate import *


def upgrade(migrate_engine):
    meta = MetaData(bind=migrate_engine)

    # users = Table('users', meta, autoload=True)
    listings = Table('listings', meta, autoload=True)
    users = Table('users', meta, autoload=True)
    listing_favorites = Table('listing_favorites', meta, autoload=True)

    ForeignKeyConstraint(
        columns=[listing_favorites.c.user_id],
        refcolumns=[users.c.id]).create()
    ForeignKeyConstraint(
        columns=[listing_favorites.c.listing_id],
        refcolumns=[listings.c.id]).create()
    pass


def downgrade(migrate_engine):
    meta = MetaData(bind=migrate_engine)

    # users = Table('users', meta, autoload=True)
    listings = Table('listings', meta, autoload=True)
    users = Table('users', meta, autoload=True)
    listing_favorites = Table('listing_favorites', meta, autoload=True)

    ForeignKeyConstraint(
        columns=[listing_favorites.c.user_id],
        refcolumns=[users.c.id]).drop()
    ForeignKeyConstraint(
        columns=[listing_favorites.c.listing_id],
        refcolumns=[listings.c.id]).drop()
    pass
