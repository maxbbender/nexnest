from sqlalchemy import *
from migrate import *


meta = MetaData()
# Column('XXXX', String(120)),
securityDeposits = Table('security_deposits', meta,
                         Column('id', Integer(),
                                primary_key=True,
                                nullable=False),
                         Column('group_listing_id', Integer()),
                         Column('user_id', Integer()),
                         Column('completed', Boolean()),
                         Column('date_created', DateTime()),
                         Column('date_modified', DateTime()), schema=None)


def upgrade(migrate_engine):
    meta.bind = migrate_engine
    securityDeposits.create()

    u = Table('users', meta, autoload=True)
    gl = Table('group_listings', meta, autoload=True)

    ForeignKeyConstraint(
        columns=[securityDeposits.c.user_id],
        refcolumns=[u.c.id]).create()
    ForeignKeyConstraint(
        columns=[securityDeposits.c.group_listing_id],
        refcolumns=[gl.c.id]).create()
    pass


def downgrade(migrate_engine):
    meta.bind = migrate_engine

    u = Table('users', meta, autoload=True)
    gl = Table('group_listings', meta, autoload=True)

    ForeignKeyConstraint(
        columns=[securityDeposits.c.user_id],
        refcolumns=[u.c.id]).drop()
    ForeignKeyConstraint(
        columns=[securityDeposits.c.group_listing_id],
        refcolumns=[gl.c.id]).drop()

    securityDeposits.drop()
    pass
