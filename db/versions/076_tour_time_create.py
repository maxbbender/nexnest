from sqlalchemy import *
from migrate import *


meta = MetaData()
# Column('XXXX', String(120)),
tourTime = Table('tour_times', meta,
                 Column('tour_id', Integer(), primary_key=True, nullable=False),
                 Column('date_time_requested', DateTime(), primary_key=True, nullable=False),
                 Column('confirmed', Boolean()),
                 Column('date_created', DateTime()),
                 Column('date_modified', DateTime()))


def upgrade(migrate_engine):
    meta.bind = migrate_engine
    tourTime.create()

    # Foreign Keys
    tours = Table('tours', meta, autoload=True)
    ForeignKeyConstraint(
        columns=[tourTime.c.tour_id],
        refcolumns=[tours.c.id]).create()
    pass


def downgrade(migrate_engine):
    meta.bind = migrate_engine

    # Foreign Keys
    tours = Table('tours', meta, autoload=True)
    ForeignKeyConstraint(
        columns=[tourTime.c.tour_id],
        refcolumns=[tours.c.id]).drop()

    tourTime.drop()
    pass
