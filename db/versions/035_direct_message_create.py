from sqlalchemy import *
from migrate import *


meta = MetaData()
# Column('XXXX', String(120)),
direct_messages = Table('direct_messages', meta,
                        # Column('source_user_id', Integer(),
                        #        primary_key=True,
                        #        nullable=False),
                        Column('target_user_id', Integer(),
                               primary_key=True,
                               nullable=False),
                        Column('message_id', Integer(),
                               primary_key=True,
                               nullable=False),
                        Column('date_created', DateTime()),
                        Column('date_modified', DateTime()))


def upgrade(migrate_engine):
    meta.bind = migrate_engine
    direct_messages.create()

    # users = Table('users', meta, autoload=True)
    users = Table('users', meta, autoload=True)
    messages = Table('messages', meta, autoload=True)
    direct_message = Table('direct_messages', meta, autoload=True)

    # ForeignKeyConstraint(
    #     columns=[direct_message.c.source_user_id],
    #     refcolumns=[users.c.id]).create()
    ForeignKeyConstraint(
        columns=[direct_message.c.target_user_id],
        refcolumns=[users.c.id]).create()
    ForeignKeyConstraint(
        columns=[direct_message.c.message_id],
        refcolumns=[messages.c.id]).create()


def downgrade(migrate_engine):
    meta.bind = migrate_engine

    # users = Table('users', meta, autoload=True)
    users = Table('users', meta, autoload=True)
    messages = Table('messages', meta, autoload=True)
    direct_message = Table('direct_messages', meta, autoload=True)

    # ForeignKeyConstraint(
    #     columns=[direct_message.c.source_user_id],
    #     refcolumns=[users.c.id]).drop()
    ForeignKeyConstraint(
        columns=[direct_message.c.target_user_id],
        refcolumns=[users.c.id]).drop()
    ForeignKeyConstraint(
        columns=[direct_message.c.message_id],
        refcolumns=[messages.c.id]).drop()

    direct_messages.drop()
