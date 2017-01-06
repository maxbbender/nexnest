from sqlalchemy import *
from migrate import *


def upgrade(migrate_engine):
    meta = MetaData(bind=migrate_engine)

    # users = Table('users', meta, autoload=True)
    groups = Table('groups', meta, autoload=True)
    listings = Table('listings', meta, autoload=True)
    group_listings = Table('group_listings', meta, autoload=True)

    ForeignKeyConstraint(
        columns=[group_listings.c.group_id],
        refcolumns=[groups.c.id]).create()
    ForeignKeyConstraint(
        columns=[group_listings.c.listing_id],
        refcolumns=[listings.c.id]).create()
    pass


def downgrade(migrate_engine):
    meta = MetaData(bind=migrate_engine)

    # users = Table('users', meta, autoload=True)
    groups = Table('groups', meta, autoload=True)
    listings = Table('listings', meta, autoload=True)
    group_listings = Table('group_listings', meta, autoload=True)

    ForeignKeyConstraint(
        columns=[group_listings.c.group_id],
        refcolumns=[groups.c.id]).drop()
    ForeignKeyConstraint(
        columns=[group_listings.c.listing_id],
        refcolumns=[listings.c.id]).drop()
    pass
