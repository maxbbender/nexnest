from sqlalchemy import *
from migrate import *


def upgrade(migrate_engine):
    meta = MetaData(bind=migrate_engine)

    # users = Table('users', meta, autoload=True)
    gl = Table('group_listings', meta, autoload=True)

    newc = Column('all_leases_submitted', Boolean())

    newc.create(gl)
    pass


def downgrade(migrate_engine):
    meta = MetaData(bind=migrate_engine)

    # users = Table('users', meta, autoload=True)
    gl = Table('group_listings', meta, autoload=True)

    gl.c.all_leases_submitted.drop()
    pass
