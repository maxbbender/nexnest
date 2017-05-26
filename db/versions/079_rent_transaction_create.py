from sqlalchemy import *
from migrate import *


meta = MetaData()
# Column('XXXX', String(120)),
rentT = Table('rent_transactions', meta,
              Column('id', Integer(), primary_key=True, nullable=False),
              Column('rent_id', Integer()))


def upgrade(migrate_engine):
    meta.bind = migrate_engine
    rentT.create()

    # Foreign Keys
    transaction = Table('transactions', meta, autoload=True)
    rent = Table('rents', meta, autoload=True)
    ForeignKeyConstraint(
        columns=[rentT.c.id],
        refcolumns=[transaction.c.id]).create()
    ForeignKeyConstraint(
        columns=[rentT.c.rent_id],
        refcolumns=[rent.c.id]).create()
    pass


def downgrade(migrate_engine):
    meta.bind = migrate_engine

    # Foreign Keys
    transaction = Table('transactions', meta, autoload=True)
    rent = Table('rents', meta, autoload=True)
    ForeignKeyConstraint(
        columns=[rentT.c.id],
        refcolumns=[transaction.c.id]).drop()
    ForeignKeyConstraint(
        columns=[rentT.c.rent_id],
        refcolumns=[rent.c.id]).drop()

    rentT.drop()
    pass
