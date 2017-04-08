from sqlalchemy import *
from migrate import *


meta = MetaData()
# Column('XXXX', String(120)),
listingSchools = Table('listing_schools', meta,
                       Column('listing_id',
                              Integer(),
                              primary_key=True,
                              nullable=False),
                       Column('school_id',
                              Integer(),
                              primary_key=True,
                              nullable=False),
                       Column('driving_time',
                              Text()),
                       Column('driving_miles',
                              Text()),
                       Column('walking_time',
                              Text()),
                       Column('walking_miles',
                              Text()),)


def upgrade(migrate_engine):
    meta.bind = migrate_engine
    listingSchools.create()

    # Foreign Keys
    listings = Table('listings', meta, autoload=True)
    schools = Table('schools', meta, autoload=True)
    ForeignKeyConstraint(
        columns=[listingSchools.c.listing_id],
        refcolumns=[listings.c.id]).create()
    ForeignKeyConstraint(
        columns=[listingSchools.c.school_id],
        refcolumns=[schools.c.id]).create()
    pass


def downgrade(migrate_engine):
    meta.bind = migrate_engine

    # Foreign Keys
    listings = Table('listings', meta, autoload=True)
    schools = Table('schools', meta, autoload=True)
    ForeignKeyConstraint(
        columns=[listingSchools.c.listing_id],
        refcolumns=[listings.c.id]).drop()
    ForeignKeyConstraint(
        columns=[listingSchools.c.school_id],
        refcolumns=[schools.c.id]).drop()

    listingSchools.drop()
    pass
