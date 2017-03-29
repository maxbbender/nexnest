from sqlalchemy import *
from migrate import *


meta = MetaData()
# Column('XXXX', String(120)),
users = Table('users',
              meta,
              Column('id', Integer(),
                     primary_key=True,
                     nullable=False),
              Column('username', String(length=80)),
              Column('email', String(length=120)),
              Column('password',
                     String(length=128),
                     nullable=False),
              Column('salt', String(length=128),
                     nullable=False),
              Column('name', String(length=128)),
              Column('role', String(length=10)),
              Column('bio', Text()),
              Column('website',
                     String(length=128)),
              Column('location', String(length=128)),
              Column('phone', String(length=10)),
              Column('dob', DateTime()),
              Column('profile_image', String(length=128)),
              Column('date_created', DateTime(),
                     nullable=False),
              Column('date_modified', DateTime(),
                     nullable=False),
              Column('active', Boolean()))


def upgrade(migrate_engine):
    meta.bind = migrate_engine
    users.create()


def downgrade(migrate_engine):
    meta.bind = migrate_engine
    users.drop()
