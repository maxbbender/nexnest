from sqlalchemy import *
from migrate import *


meta = MetaData()
# Column('XXXX', String(120)),
friends = Table('friends', meta,
                Column('source_user_id', Integer(),
                       primary_key=True,
                       nullable=False),
                Column('target_user_id', Integer(),
                       primary_key=True,
                       nullable=False))


def upgrade(migrate_engine):
    meta.bind = migrate_engine
    friends.create()


def downgrade(migrate_engine):
    meta.bind = migrate_engine
    friends.drop()
