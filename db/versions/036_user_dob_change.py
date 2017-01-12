from sqlalchemy import *
from migrate import *


def upgrade(migrate_engine):
    meta = MetaData(bind=migrate_engine)

    # users = Table('users', meta, autoload=True)
    users = Table('users', meta, autoload=True)

    # users.c.password.drop()
    users.c.dob.drop()

    dob = Column("dob", Date())

    dob.create(users)

    pass


def downgrade(migrate_engine):
    meta = MetaData(bind=migrate_engine)

    # users = Table('users', meta, autoload=True)
    users = Table('users', meta, autoload=True)

    users.c.dob.drop()

    # password = Column("password", String(128), nullable=False)

    dob = Column("dob", DateTime())

    # password.create(users)
    dob.create(users)
    pass
