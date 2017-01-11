from sqlalchemy import *
from migrate import *


meta = MetaData()
# Column('XXXX', String(120)),
tours = Table('tours', meta,
              Column('id', Integer(),
                     primary_key=True,
                     nullable=False),
              Column('listing_id', Integer()),
              Column('group_id', Integer()),
              Column('time_requested', DateTime()),
              Column('description', Text()),
              Column('date_created', DateTime()),
              Column('date_modified', DateTime()))


def upgrade(migrate_engine):
    meta.bind = migrate_engine
    tours.create()

    tour = Table('tours', meta, autoload=True)
    listings = Table('listings', meta, autoload=True)
    groups = Table('groups', meta, autoload=True)

    ForeignKeyConstraint(
        columns=[tour.c.listing_id],
        refcolumns=[listings.c.id]).create()
    ForeignKeyConstraint(
        columns=[tour.c.group_id],
        refcolumns=[groups.c.id]).create()
    pass


def downgrade(migrate_engine):
    meta.bind = migrate_engine

    tour = Table('tours', meta, autoload=True)
    listings = Table('listings', meta, autoload=True)
    groups = Table('groups', meta, autoload=True)

    ForeignKeyConstraint(
        columns=[tour.c.listing_id],
        refcolumns=[listings.c.id]).drop()
    ForeignKeyConstraint(
        columns=[tour.c.group_id],
        refcolumns=[groups.c.id]).drop()
    tours.drop()
    pass
