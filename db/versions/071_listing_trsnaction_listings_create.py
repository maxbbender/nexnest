from sqlalchemy import *
from migrate import *


meta = MetaData()

ltl = Table('listing_transaction_listings', meta,
            Column('id', Integer(),
                   primary_key=True,
                   nullable=False),
            Column('listing_id', Integer()),
            Column('plan', String(length=50)),
            Column('listing_transactions_id', Integer()))


def upgrade(migrate_engine):
    meta.bind = migrate_engine
    ltl.create()

    listings = Table('listings', meta, autoload=True)
    listingTransactions = Table('listing_transactions', meta, autoload=True)

    ForeignKeyConstraint(
        columns=[ltl.c.listing_id],
        refcolumns=[listings.c.id]).create()
    ForeignKeyConstraint(
        columns=[ltl.c.listing_transactions_id],
        refcolumns=[listingTransactions.c.id]).create()
    pass


def downgrade(migrate_engine):
    meta.bind = migrate_engine

    listings = Table('listings', meta, autoload=True)
    listingTransactions = Table('listing_transactions', meta, autoload=True)

    ForeignKeyConstraint(
        columns=[ltl.c.listing_id],
        refcolumns=[listings.c.id]).drop()
    ForeignKeyConstraint(
        columns=[ltl.c.listing_transactions_id],
        refcolumns=[listingTransactions.c.id]).drop()
    ltl.drop()
    pass
