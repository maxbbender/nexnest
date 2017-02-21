from sqlalchemy import *
from migrate import *


meta = MetaData()
# Column('XXXX', String(120)),
notifications = Table('notifications', meta,
                      Column('id', Integer(),
                             primary_key=True,
                             nullable=False),
                      Column('target_user_id', Integer()),
                      Column('target_model_id', Integer()),
                      Column('viewed', Boolean()),
                      Column('date_created', DateTime()),
                      Column('date_modified', DateTime()),
                      Column('type', String(length=128)))


def upgrade(migrate_engine):
    meta.bind = migrate_engine
    notifications.create()

    users = Table('users', meta, autoload=True)

    ForeignKeyConstraint(
        columns=[notifications.c.target_user_id],
        refcolumns=[users.c.id]).create()
    pass


def downgrade(migrate_engine):
    meta.bind = migrate_engine

    users = Table('users', meta, autoload=True)
    ForeignKeyConstraint(
        columns=[notifications.c.target_user_id],
        refcolumns=[users.c.id]).drop()

    notifications.drop()
    pass
