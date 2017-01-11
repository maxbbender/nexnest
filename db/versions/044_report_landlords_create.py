from sqlalchemy import *
from migrate import *


meta = MetaData()
# Column('XXXX', String(120)),
report_landlords = Table('report_landlords', meta,
                         Column('report_id', Integer(),
                                primary_key=True,
                                nullable=False),
                         Column('landlord_id', Integer(),
                                primary_key=True,
                                nullable=False))


def upgrade(migrate_engine):
    meta.bind = migrate_engine
    report_landlords.create()

    report_landlord = Table('report_landlords', meta, autoload=True)
    reports = Table('reports', meta, autoload=True)
    landlords = Table('landlords', meta, autoload=True)

    ForeignKeyConstraint(
        columns=[report_landlord.c.report_id],
        refcolumns=[reports.c.id]).create()
    ForeignKeyConstraint(
        columns=[report_landlord.c.landlord_id],
        refcolumns=[landlords.c.user_id]).create()
    pass


def downgrade(migrate_engine):
    meta.bind = migrate_engine

    report_landlord = Table('report_landlords', meta, autoload=True)
    reports = Table('reports', meta, autoload=True)
    landlords = Table('landlords', meta, autoload=True)

    ForeignKeyConstraint(
        columns=[report_landlord.c.report_id],
        refcolumns=[reports.c.id]).drop()
    ForeignKeyConstraint(
        columns=[report_landlord.c.landlord_id],
        refcolumns=[landlords.c.user_id]).drop()

    report_landlords.drop()
    pass
