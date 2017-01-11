from sqlalchemy import *
from migrate import *


def downgrade(migrate_engine):
    meta = MetaData(bind=migrate_engine)

    # users = Table('users', meta, autoload=True)
    group_listings = Table('group_listings', meta, autoload=True)

    # users.c.password.drop()
    group_listings.c.accepted.drop()
    group_listings.c.show.drop()
    group_listings.c.completed.drop()
    group_listings.c.date_created.drop()
    pass


def upgrade(migrate_engine):
    meta = MetaData(bind=migrate_engine)

    # users = Table('users', meta, autoload=True)
    group_listings = Table('group_listings', meta, autoload=True)

    # password = Column("password", String(128), nullable=False)
    accepted = Column("accepted", Boolean())
    completed = Column("completed", Boolean())
    show = Column("show", Boolean())
    date_created = Column('date_created', String(length=128), nullable=False)

    # password.create(users)
    accepted.create(group_listings)
    show.create(group_listings)
    completed.create(group_listings)
    date_created.create(group_listings)
    pass
