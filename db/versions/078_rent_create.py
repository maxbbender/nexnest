from sqlalchemy import *
from migrate import *


meta = MetaData()
# Column('XXXX', String(120)),
rents = Table('rents', meta,
              Column('id', Integer(), primary_key=True, nullable=False),
              Column('house_id', Integer()),
              Column('user_id', Integer()),
              Column('date_due', Date()),
              Column('amount', Integer()),
              Column('completed', Boolean()),
              Column('date_created', DateTime()),
              Column('date_modified', DateTime()))


def upgrade(migrate_engine):
    meta.bind = migrate_engine
    rents.create()

    # Foreign Keys
    house = Table('houses', meta, autoload=True)
    users = Table('users', meta, autoload=True)
    ForeignKeyConstraint(
        columns=[rents.c.house_id],
        refcolumns=[house.c.id]).create()
    ForeignKeyConstraint(
        columns=[rents.c.user_id],
        refcolumns=[users.c.id]).create()
    pass


def downgrade(migrate_engine):
    meta.bind = migrate_engine

    # Foreign Keys
    house = Table('houses', meta, autoload=True)
    users = Table('users', meta, autoload=True)
    ForeignKeyConstraint(
        columns=[rents.c.house_id],
        refcolumns=[house.c.id]).drop()
    ForeignKeyConstraint(
        columns=[rents.c.user_id],
        refcolumns=[users.c.id]).drop()

    rents.drop()
    pass
