from sqlalchemy import *
from migrate import *


meta = MetaData()
# Column('XXXX', String(120)),
messages = Table('messages', meta,
                 Column('id', Integer(),
                        primary_key=True,
                        nullable=False),
                 Column('content', Text()),
                 Column('user_id', Integer()),
                 Column('date_created', DateTime()),
                 Column('date_modified', DateTime()))


def upgrade(migrate_engine):
    meta.bind = migrate_engine
    messages.create()


def downgrade(migrate_engine):
    meta.bind = migrate_engine
    messages.drop()
