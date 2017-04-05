from sqlalchemy import *
from migrate import *


meta = MetaData()
# Column('XXXX', String(120)),
cupons = Table('cupons', meta,
               Column('id', Integer(),
                      primary_key=True,
                      nullable=False),
               Column('cupon_key', Text()),
               Column('unlimited', Boolean()),
               Column('percentage_off', Integer()),
               Column('uses', Integer()),
               Column('date_created', DateTime()),
               Column('date_modified', DateTime()),
               UniqueConstraint('cupon_key'))


def upgrade(migrate_engine):
    meta.bind = migrate_engine
    cupons.create()
    pass


def downgrade(migrate_engine):
    meta.bind = migrate_engine
    cupons.drop()
    pass
