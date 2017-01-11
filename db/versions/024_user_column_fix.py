from sqlalchemy import *
from migrate import *


def upgrade(migrate_engine):
    meta = MetaData(bind=migrate_engine)

    # users = Table('users', meta, autoload=True)
    users = Table('users', meta, autoload=True)

    fname = Column("fname", String(128), nullable=False)
    lname = Column("lname", String(128), nullable=False)

    users.c.name.drop()
    fname.create(users)
    lname.create(users)

    pass


def downgrade(migrate_engine):
    meta = MetaData(bind=migrate_engine)

    # users = Table('users', meta, autoload=True)
    users = Table('users', meta, autoload=True)

    # password = Column("password", String(128), nullable=False)
    name = Column("name", String(128), nullable=False)

    # password.create(users)
    name.create(users)

    users.c.fname.drop()
    users.c.lname.drop()

    pass
