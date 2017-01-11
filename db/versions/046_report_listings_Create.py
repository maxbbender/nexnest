from sqlalchemy import *
from migrate import *


meta = MetaData()
# Column('XXXX', String(120)),
report_listings = Table('report_listings', meta,
                        Column('report_id', Integer(),
                               primary_key=True,
                               nullable=False),
                        Column('listing_id', Integer(),
                               primary_key=True,
                               nullable=False))


def upgrade(migrate_engine):
    meta.bind = migrate_engine
    report_listings.create()

    report_listing = Table('report_listings', meta, autoload=True)
    reports = Table('reports', meta, autoload=True)
    listings = Table('listings', meta, autoload=True)

    ForeignKeyConstraint(
        columns=[report_listing.c.report_id],
        refcolumns=[reports.c.id]).create()
    ForeignKeyConstraint(
        columns=[report_listing.c.listing_id],
        refcolumns=[listings.c.id]).create()
    pass


def downgrade(migrate_engine):
    meta.bind = migrate_engine

    report_listing = Table('report_listings', meta, autoload=True)
    reports = Table('reports', meta, autoload=True)
    listings = Table('listings', meta, autoload=True)

    ForeignKeyConstraint(
        columns=[report_listing.c.report_id],
        refcolumns=[reports.c.id]).drop()
    ForeignKeyConstraint(
        columns=[report_listing.c.listing_id],
        refcolumns=[listings.c.id]).drop()

    report_listings.drop()
    pass
