from sqlalchemy import *
from migrate import *


meta = MetaData()
# Column('XXXX', String(120)),
tour_messages = Table('tour_messages', meta,
                      Column('tour_id', Integer(),
                             primary_key=True,
                             nullable=False),
                      Column('message_id', Integer(),
                             primary_key=True,
                             nullable=False),
                      Column('date_created', DateTime()),
                      Column('date_modified', DateTime()))


def upgrade(migrate_engine):
    meta.bind = migrate_engine
    tour_messages.create()

    tour = Table('tours', meta, autoload=True)
    messages = Table('messages', meta, autoload=True)
    tour_message = Table('tour_messages', meta, autoload=True)

    ForeignKeyConstraint(
        columns=[tour_message.c.tour_id],
        refcolumns=[tour.c.id]).create()
    ForeignKeyConstraint(
        columns=[tour_message.c.message_id],
        refcolumns=[messages.c.id]).create()
    pass


def downgrade(migrate_engine):
    meta.bind = migrate_engine

    tour = Table('tours', meta, autoload=True)
    messages = Table('messages', meta, autoload=True)
    tour_message = Table('tour_messages', meta, autoload=True)

    ForeignKeyConstraint(
        columns=[tour_message.c.tour_id],
        refcolumns=[tour.c.id]).drop()
    ForeignKeyConstraint(
        columns=[tour_message.c.message_id],
        refcolumns=[messages.c.id]).drop()
    tour_messages.drop()
    pass
