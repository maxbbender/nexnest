from sqlalchemy import *
from migrate import *


meta = MetaData()
# Column('XXXX', String(120)),
group_users = Table('group_users', meta,
                    Column('group_id', Integer(),
                           primary_key=True,
                           nullable=False),
                    Column('user_id', Integer(),
                           primary_key=True,
                           nullable=False))


def upgrade(migrate_engine):
    meta.bind = migrate_engine
    group_users.create()


def downgrade(migrate_engine):
    meta.bind = migrate_engine
    group_users.drop()
