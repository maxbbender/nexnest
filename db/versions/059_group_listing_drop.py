from sqlalchemy import *
from migrate import *


def upgrade(migrate_engine):
    meta = MetaData(bind=migrate_engine)

    # users = Table('users', meta, autoload=True)
    gl = Table('group_listings', meta, autoload=True)

    # users.c.password.drop()
    gl.c.req_description.drop()
    pass


def downgrade(migrate_engine):
    meta = MetaData(bind=migrate_engine)

    # users = Table('users', meta, autoload=True)
    gl = Table('group_listings', meta, autoload=True)

    # password = Column("password", String(128), nullable=False)
    req_description = Column("req_description", Text())

    # password.create(users)
    req_description.create(gl)
    pass
