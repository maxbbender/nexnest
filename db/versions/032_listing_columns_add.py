from sqlalchemy import *
from migrate import *


def downgrade(migrate_engine):
    meta = MetaData(bind=migrate_engine)

    # users = Table('users', meta, autoload=True)
    listings = Table('listings', meta, autoload=True)

    # users.c.password.drop()
    listings.c.time_period.drop()
    listings.c.apartment_number.drop()
    listings.c.disabled.drop()
    pass


def upgrade(migrate_engine):
    meta = MetaData(bind=migrate_engine)

    # users = Table('users', meta, autoload=True)
    listings = Table('listings', meta, autoload=True)

    # password = Column("password", String(128), nullable=False)
    time_period = Column("time_period", String(8))
    apartment_number = Column("apartment_number", Integer())
    disabled = Column("disabled", Boolean())

    # password.create(users)
    time_period.create(listings)
    apartment_number.create(listings)
    disabled.create(listings)
    pass
