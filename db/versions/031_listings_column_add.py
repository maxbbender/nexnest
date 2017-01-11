from sqlalchemy import *
from migrate import *


def downgrade(migrate_engine):
    meta = MetaData(bind=migrate_engine)

    # users = Table('users', meta, autoload=True)
    listings = Table('listings', meta, autoload=True)

    # users.c.password.drop()
    listings.c.active.drop()
    listings.c.show.drop()
    listings.c.description.drop()
    listings.c.num_half_baths.drop()
    listings.c.num_full_baths.drop()
    pass


def upgrade(migrate_engine):
    meta = MetaData(bind=migrate_engine)

    # users = Table('users', meta, autoload=True)
    listings = Table('listings', meta, autoload=True)

    # password = Column("password", String(128), nullable=False)
    description = Column("description", Text())
    num_full_baths = Column("num_full_baths", Integer())
    num_half_baths = Column("num_half_baths", Integer())
    active = Column("active", Boolean())
    show = Column("show", Boolean())

    # password.create(users)
    description.create(listings)
    show.create(listings)
    active.create(listings)
    num_half_baths.create(listings)
    num_full_baths.create(listings)
    pass
