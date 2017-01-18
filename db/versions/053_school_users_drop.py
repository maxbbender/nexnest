from sqlalchemy import *
from migrate import *


meta = MetaData()
# Column('XXXX', String(120)),
school_users = Table('school_users', meta,
                     Column('user_id',
                            Integer(),
                            primary_key=True,
                            nullable=False),
                     Column('school_id', Integer(),
                            primary_key=True,
                            nullable=False))


def upgrade(migrate_engine):
    meta.bind = migrate_engine
    school_users.drop()


def downgrade(migrate_engine):
    meta.bind = migrate_engine
    school_users.create()
