from sqlalchemy import *
from migrate import *


meta = MetaData()
# Column('XXXX', String(120)),
glf = Table('group_listing_favorites', meta,
            Column('group_id', Integer(),
                   primary_key=True,
                   nullable=False),
            Column('listing_id', Integer(),
                   primary_key=True,
                   nullable=False),
            Column('date_created', DateTime()))


def upgrade(migrate_engine):
    meta.bind = migrate_engine
    glf.create()

    gr = Table('groups', meta, autoload=True)
    lis = Table('listings', meta, autoload=True)

    ForeignKeyConstraint(
        columns=[glf.c.group_id],
        refcolumns=[gr.c.id]).create()
    ForeignKeyConstraint(
        columns=[glf.c.listing_id],
        refcolumns=[lis.c.id]).create()
    pass


def downgrade(migrate_engine):
    meta.bind = migrate_engine

    gr = Table('groups', meta, autoload=True)
    lis = Table('listings', meta, autoload=True)

    ForeignKeyConstraint(
        columns=[glf.c.group_id],
        refcolumns=[gr.c.id]).drop()
    ForeignKeyConstraint(
        columns=[glf.c.listing_id],
        refcolumns=[lis.c.id]).drop()
    glf.drop()
    pass
