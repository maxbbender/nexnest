from sqlalchemy import *
from migrate import *


meta = MetaData()
listingTransactions = Table('listing_transactions', meta,
                            Column('id', Integer(),
                                   primary_key=True,
                                   nullable=False),
                            Column('listing_id', Integer()),
                            Column('plan', String(length=50)))


def upgrade(migrate_engine):
    meta.bind = migrate_engine
    listingTransactions.create()

    listings = Table('listings', meta, autoload=True)
    transactions = Table('transactions', meta, autoload=True)

    ForeignKeyConstraint(
        columns=[listingTransactions.c.id],
        refcolumns=[transactions.c.id]).create()

    ForeignKeyConstraint(
        columns=[listingTransactions.c.listing_id],
        refcolumns=[listings.c.id]).create()
    pass


def downgrade(migrate_engine):
    meta.bind = migrate_engine

    listings = Table('listings', meta, autoload=True)
    transactions = Table('transactions', meta, autoload=True)

    ForeignKeyConstraint(
        columns=[listingTransactions.c.id],
        refcolumns=[transactions.c.id]).drop()

    ForeignKeyConstraint(
        columns=[listingTransactions.c.listing_id],
        refcolumns=[listings.c.id]).drop()

    listingTransactions.drop()
    pass
