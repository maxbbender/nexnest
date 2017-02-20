from sqlalchemy import *
from migrate import *


def upgrade(migrate_engine):
    meta = MetaData(bind=migrate_engine)

    # users = Table('users', meta, autoload=True)
    listings = Table('listings', meta, autoload=True)

    # password = Column("password", String(128), nullable=False)
    ptype = Column("property_type", Text())
    rent = Column("rent_due", String(20))
    maintenance = Column('maintenance', Boolean())

    ptype.create(listings)
    rent.create(listings)
    maintenance.create(listings)

    pass


def downgrade(migrate_engine):
    meta = MetaData(bind=migrate_engine)

    # users = Table('users', meta, autoload=True)
    listings = Table('listings', meta, autoload=True)

    # users.c.password.drop()
    listings.c.ptype.drop()
    listings.c.rent.drop()
    listings.c.maintenance.drop()

    pass
