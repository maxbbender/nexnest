from sqlalchemy import *
from migrate import *


meta = MetaData()
# Column('XXXX', String(120)),
houseMessage = Table('house_messages', meta,
                     Column('house_id', Integer(),
                            primary_key=True,
                            nullable=False),
                     Column('message_id', Integer(),
                            primary_key=True,
                            nullable=False))


def upgrade(migrate_engine):
    meta.bind = migrate_engine
    houseMessage.create()

    houseMessages = Table('house_messages', meta, autoload=True)
    houses = Table('houses', meta, autoload=True)
    messages = Table('messages', meta, autoload=True)

    ForeignKeyConstraint(
        columns=[houseMessages.c.house_id],
        refcolumns=[houses.c.id]).create()
    ForeignKeyConstraint(
        columns=[houseMessages.c.message_id],
        refcolumns=[messages.c.id]).create()
    pass


def downgrade(migrate_engine):
    meta.bind = migrate_engine

    houseMessages = Table('house_messages', meta, autoload=True)
    houses = Table('houses', meta, autoload=True)
    messages = Table('messages', meta, autoload=True)

    ForeignKeyConstraint(
        columns=[houseMessages.c.house_id],
        refcolumns=[houses.c.id]).drop()
    ForeignKeyConstraint(
        columns=[houseMessages.c.message_id],
        refcolumns=[messages.c.id]).drop()

    houseMessage.drop()

    pass
