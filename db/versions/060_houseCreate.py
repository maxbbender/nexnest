from sqlalchemy import *
from migrate import *


meta = MetaData()
# Column('XXXX', String(120)),
house = Table('houses', meta,
              Column('id', Integer(),
                     primary_key=True,
                     nullable=False),
              Column('listing_id',
                     Integer()),
              Column('group_id',
                     Integer()),
              Column('date_created', DateTime()),
              Column('date_modified', DateTime()))


def upgrade(migrate_engine):
    meta.bind = migrate_engine
    house.create()

    houses = Table('houses', meta, autoload=True)
    listings = Table('listings', meta, autoload=True)
    groups = Table('groups', meta, autoload=True)

    ForeignKeyConstraint(
        columns=[houses.c.group_id],
        refcolumns=[groups.c.id]).create()
    ForeignKeyConstraint(
        columns=[houses.c.listing_id],
        refcolumns=[listings.c.id]).create()
    pass


def downgrade(migrate_engine):
    meta.bind = migrate_engine

    houses = Table('houses', meta, autoload=True)
    listings = Table('listings', meta, autoload=True)
    groups = Table('groups', meta, autoload=True)

    ForeignKeyConstraint(
        columns=[houses.c.group_id],
        refcolumns=[groups.c.id]).drop()
    ForeignKeyConstraint(
        columns=[houses.c.listing_id],
        refcolumns=[listings.c.id]).drop()
    house.drop()

    pass
