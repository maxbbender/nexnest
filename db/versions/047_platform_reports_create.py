from sqlalchemy import *
from migrate import *


meta = MetaData()
# Column('XXXX', String(120)),
platform_reports = Table('platform_reports', meta,
                         Column('report_id', Integer(),
                                primary_key=True,
                                nullable=False))


def upgrade(migrate_engine):
    meta.bind = migrate_engine
    platform_reports.create()

    reports = Table('reports', meta, autoload=True)
    platform_report = Table('platform_reports', meta, autoload=True)

    ForeignKeyConstraint(
        columns=[platform_report.c.report_id],
        refcolumns=[reports.c.id]).create()
    pass


def downgrade(migrate_engine):
    meta.bind = migrate_engine

    reports = Table('reports', meta, autoload=True)
    platform_report = Table('platform_reports', meta, autoload=True)

    ForeignKeyConstraint(
        columns=[platform_report.c.report_id],
        refcolumns=[reports.c.id]).drop()

    platform_reports.drop()
    pass
