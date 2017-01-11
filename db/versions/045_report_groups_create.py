from sqlalchemy import *
from migrate import *


meta = MetaData()
# Column('XXXX', String(120)),
report_groups = Table('report_groups', meta,
                      Column('report_id', Integer(),
                             primary_key=True,
                             nullable=False),
                      Column('group_id', Integer(),
                             primary_key=True,
                             nullable=False))


def upgrade(migrate_engine):
    meta.bind = migrate_engine
    report_groups.create()

    report_group = Table('report_groups', meta, autoload=True)
    reports = Table('reports', meta, autoload=True)
    groups = Table('groups', meta, autoload=True)

    ForeignKeyConstraint(
        columns=[report_group.c.report_id],
        refcolumns=[reports.c.id]).create()
    ForeignKeyConstraint(
        columns=[report_group.c.group_id],
        refcolumns=[groups.c.id]).create()
    pass


def downgrade(migrate_engine):
    meta.bind = migrate_engine

    report_group = Table('report_groups', meta, autoload=True)
    reports = Table('reports', meta, autoload=True)
    groups = Table('groups', meta, autoload=True)

    ForeignKeyConstraint(
        columns=[report_group.c.report_id],
        refcolumns=[reports.c.id]).drop()
    ForeignKeyConstraint(
        columns=[report_group.c.group_id],
        refcolumns=[groups.c.id]).drop()
    report_groups.drop()
    pass
