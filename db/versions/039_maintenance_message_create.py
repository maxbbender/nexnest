from sqlalchemy import *
from migrate import *


meta = MetaData()
# Column('XXXX', String(120)),
maintenance_messages = Table('maintenance_messages', meta,
                             Column('message_id', Integer(),
                                    primary_key=True,
                                    nullable=False),
                             Column('maintenance_id', Integer(),
                                    primary_key=True,
                                    nullable=False))


def upgrade(migrate_engine):
    meta.bind = migrate_engine
    maintenance_messages.create()

    maintenance_message = Table('maintenance_messages', meta, autoload=True)
    maintenances = Table('maintenances', meta, autoload=True)
    messages = Table('messages', meta, autoload=True)

    ForeignKeyConstraint(
        columns=[maintenance_message.c.message_id],
        refcolumns=[messages.c.id]).create()
    ForeignKeyConstraint(
        columns=[maintenance_message.c.maintenance_id],
        refcolumns=[maintenances.c.id]).create()
    pass


def downgrade(migrate_engine):
    meta.bind = migrate_engine

    maintenance_message = Table('maintenance_messages', meta, autoload=True)
    maintenances = Table('maintenances', meta, autoload=True)
    messages = Table('messages', meta, autoload=True)

    ForeignKeyConstraint(
        columns=[maintenance_message.c.message_id],
        refcolumns=[messages.c.id]).create()
    ForeignKeyConstraint(
        columns=[maintenance_message.c.maintenance_id],
        refcolumns=[maintenances.c.id]).create()

    maintenance_messages.drop()
