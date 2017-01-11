from sqlalchemy import *
from migrate import *


meta = MetaData()
# Column('XXXX', String(120)),
group_messages = Table('group_messages', meta,
                       Column('group_id', Integer(),
                              primary_key=True,
                              nullable=False),
                       Column('message_id', Integer(),
                              primary_key=True,
                              nullable=False),
                       Column('date_created', DateTime()),
                       Column('date_modified', DateTime()))


def upgrade(migrate_engine):
    meta.bind = migrate_engine
    group_messages.create()

    group_message = Table('group_messages', meta, autoload=True)
    groups = Table('groups', meta, autoload=True)
    messages = Table('messages', meta, autoload=True)

    ForeignKeyConstraint(
        columns=[group_message.c.message_id],
        refcolumns=[messages.c.id]).create()
    ForeignKeyConstraint(
        columns=[group_message.c.group_id],
        refcolumns=[groups.c.id]).create()
    pass


def downgrade(migrate_engine):
    meta.bind = migrate_engine

    group_message = Table('group_messages', meta, autoload=True)
    groups = Table('groups', meta, autoload=True)
    messages = Table('messages', meta, autoload=True)

    ForeignKeyConstraint(
        columns=[group_message.c.message_id],
        refcolumns=[messages.c.id]).drop()
    ForeignKeyConstraint(
        columns=[group_message.c.group_id],
        refcolumns=[groups.c.id]).drop()
    group_messages.drop()
    pass
