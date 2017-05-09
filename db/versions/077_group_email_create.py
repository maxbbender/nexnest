from sqlalchemy import *
from migrate import *


meta = MetaData()
# Column('XXXX', String(120)),
groupEmails = Table('group_emails', meta,
                    Column('id', Integer(), primary_key=True, nullable=False),
                    Column('group_id', Integer()),
                    Column('email', Text()),
                    Column('date_created', DateTime()),
                    Column('date_modified', DateTime()))


def upgrade(migrate_engine):
    meta.bind = migrate_engine
    groupEmails.create()

    # Foreign Keys
    groups = Table('groups', meta, autoload=True)
    ForeignKeyConstraint(
        columns=[groupEmails.c.group_id],
        refcolumns=[groups.c.id]).create()
    pass


def downgrade(migrate_engine):
    meta.bind = migrate_engine

    # Foreign Keys
    groups = Table('groups', meta, autoload=True)
    ForeignKeyConstraint(
        columns=[groupEmails.c.group_id],
        refcolumns=[groups.c.id]).create()

    groupEmails.drop()
    pass
