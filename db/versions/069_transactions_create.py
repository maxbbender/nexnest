from sqlalchemy import *
from migrate import *


meta = MetaData()

transactions = Table('transactions',
                     meta,
                     Column('id', Integer(),
                            primary_key=True,
                            nullable=False),
                     Column('braintree_transaction_id', Text()),
                     Column('status', String(length=128)),
                     Column('success', Boolean()),
                     Column('user_id', Integer()),
                     Column('total', Float()),
                     Column('type', String(length=60)),
                     Column('date_created', DateTime()),
                     Column('date_modified', DateTime()))


def upgrade(migrate_engine):
    meta.bind = migrate_engine
    transactions.create()

    users = Table('users', meta, autoload=True)

    ForeignKeyConstraint(
        columns=[transactions.c.user_id],
        refcolumns=[users.c.id]).create()
    pass


def downgrade(migrate_engine):
    meta.bind = migrate_engine
    users = Table('users', meta, autoload=True)

    ForeignKeyConstraint(
        columns=[transactions.c.user_id],
        refcolumns=[users.c.id]).drop()

    transactions.drop()
    pass
