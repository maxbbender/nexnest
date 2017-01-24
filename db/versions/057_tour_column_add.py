from sqlalchemy import *
from migrate import *


def downgrade(migrate_engine):
    meta = MetaData(bind=migrate_engine)

    # users = Table('users', meta, autoload=True)
    tours = Table('tours', meta, autoload=True)

    # users.c.password.drop()
    tours.c.tour_confirmed.drop()
    tours.c.last_requested.drop()
    pass


def upgrade(migrate_engine):
    meta = MetaData(bind=migrate_engine)

    # users = Table('users', meta, autoload=True)
    tours = Table('tours', meta, autoload=True)

    # password = Column("password", String(128), nullable=False)
    tour_confirmed = Column("tour_confirmed", Boolean())
    last_requested = Column("last_requested", String(8))

    # password.create(users)
    tour_confirmed.create(tours)
    last_requested.create(tours)
    pass
