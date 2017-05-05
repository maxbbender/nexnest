from sqlalchemy import *
from migrate import *


meta = MetaData()
# Column('XXXX', String(120)),
avail = Table('availability', meta,
              Column('landlord_id', Integer(),
                     primary_key=True, nullable=False),
              Column('time', Time(),
                     primary_key=True, nullable=False),
              Column('day', Text(), primary_key=True, nullable=False))


def upgrade(migrate_engine):
    meta.bind = migrate_engine
    avail.create()

    # Foreign Keys
    lan = Table('landlords', meta, autoload=True)
    ForeignKeyConstraint(
        columns=[avail.c.landlord_id],
        refcolumns=[lan.c.user_id]).create()
    pass


def downgrade(migrate_engine):
    meta.bind = migrate_engine

    # Foreign Keys
    lan = Table('landlords', meta, autoload=True)
    ForeignKeyConstraint(
        columns=[avail.c.landlord_id],
        refcolumns=[lan.c.user_id]).drop()

    avail.drop()
    pass
