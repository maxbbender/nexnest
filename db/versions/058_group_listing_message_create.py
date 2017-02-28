from sqlalchemy import *
from migrate import *


meta = MetaData()
# Column('XXXX', String(120)),
glm = Table('group_listing_messages', meta,
            Column('groupListingID', Integer(),
                   primary_key=True,
                   nullable=False),
            Column('messageID', Integer(),
                   primary_key=True,
                   nullable=False))


def upgrade(migrate_engine):
    meta.bind = migrate_engine
    glm.create()

    messages = Table('messages', meta, autoload=True)
    glm2 = Table('group_listing_messages', meta, autoload=True)
    gl = Table('group_listings', meta, autoload=True)

    ForeignKeyConstraint(
        columns=[glm2.c.messageID],
        refcolumns=[messages.c.id]).create()

    ForeignKeyConstraint(
        columns=[glm2.c.groupListingID],
        refcolumns=[gl.c.id]).create()
    pass


def downgrade(migrate_engine):
    meta.bind = migrate_engine

    messages = Table('messages', meta, autoload=True)
    glm2 = Table('group_listing_messages', meta, autoload=True)
    gl = Table('group_listings', meta, autoload=True)

    ForeignKeyConstraint(
        columns=[glm2.c.messageID],
        refcolumns=[messages.c.id]).drop()

    ForeignKeyConstraint(
        columns=[glm2.c.groupListingID],
        refcolumns=[gl.c.id]).drop()
    glm.drop()

    pass
