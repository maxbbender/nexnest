from sqlalchemy import *
from migrate import *


meta = MetaData()
# Column('XXXX', String(120)),
user_roles = Table('user_roles', meta,
                   Column('user_id', Integer(),
                          primary_key=True,
                          nullable=False),
                   Column('role_id', Integer(),
                          primary_key=True,
                          nullable=False),
                   Column('date_created', DateTime()),
                   Column('date_modified', DateTime()))


def downgrade(migrate_engine):
    meta.bind = migrate_engine
    user_roles.create()


def upgrade(migrate_engine):
    meta.bind = migrate_engine
    user_roles.drop()
