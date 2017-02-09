from sqlalchemy import *
from migrate import *


def upgrade(migrate_engine):
    meta = MetaData(bind=migrate_engine)

    # users = Table('users', meta, autoload=True)
    mnt = Table('maintenances', meta, autoload=True)

    # users.c.password.drop()
    mnt.c.listing_id.drop()

    house_id = Column("house_id", Integer())

    house_id.create(mnt)

    pass


def downgrade(migrate_engine):
    meta = MetaData(bind=migrate_engine)

    # users = Table('users', meta, autoload=True)
    mnt = Table('maintenances', meta, autoload=True)

    # users.c.password.drop()
    mnt.c.house_id.drop()

    listing_id = Column("listing_id", Integer())

    listing_id.create(mnt)
    pass
