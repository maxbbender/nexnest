from sqlalchemy import *
from migrate import *


meta = MetaData()
# Column('XXXX', String(120)),
maintenances = Table('maintenances', meta,
                     Column('id', Integer(),
                            primary_key=True,
                            nullable=False),
                     Column('status', String(length=10)),
                     Column('request_type', String(length=20)),
                     Column('details', Text()),
                     Column('listing_id', Integer()),
                     Column('date_created', DateTime()),
                     Column('date_modified', DateTime()))


def upgrade(migrate_engine):
    meta.bind = migrate_engine
    maintenances.create()

    # users = Table('users', meta, autoload=True)
    maintenance = Table('maintenances', meta, autoload=True)
    listings = Table('listings', meta, autoload=True)

    ForeignKeyConstraint(
        columns=[maintenance.c.listing_id],
        refcolumns=[listings.c.id]).create()


def downgrade(migrate_engine):
    meta.bind = migrate_engine

    # users = Table('users', meta, autoload=True)
    maintenance = Table('maintenances', meta, autoload=True)
    listings = Table('listings', meta, autoload=True)

    ForeignKeyConstraint(
        columns=[maintenance.c.listing_id],
        refcolumns=[listings.c.id]).drop()

    maintenances.drop()
