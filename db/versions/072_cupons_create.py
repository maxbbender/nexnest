from sqlalchemy import *
from migrate import *


meta = MetaData()
# Column('XXXX', String(120)),
coupons = Table('coupons', meta,
               Column('id', Integer(),
                      primary_key=True,
                      nullable=False),
               Column('coupon_key', Text()),
               Column('unlimited', Boolean()),
               Column('percentage_off', Integer()),
               Column('uses', Integer()),
               Column('date_created', DateTime()),
               Column('date_modified', DateTime()),
               UniqueConstraint('coupon_key'))


def upgrade(migrate_engine):
    meta.bind = migrate_engine
    coupons.create()
    pass


def downgrade(migrate_engine):
    meta.bind = migrate_engine
    coupons.drop()
    pass
