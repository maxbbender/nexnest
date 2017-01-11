from sqlalchemy import *
from migrate import *


def downgrade(migrate_engine):
    meta = MetaData(bind=migrate_engine)

    # users = Table('users', meta, autoload=True)
    friends = Table('friends', meta, autoload=True)

    # users.c.password.drop()
    friends.c.accepted.drop()
    pass


def upgrade(migrate_engine):
    meta = MetaData(bind=migrate_engine)

    # users = Table('users', meta, autoload=True)
    friends = Table('friends', meta, autoload=True)

    # password = Column("password", String(128), nullable=False)
    accepted = Column("accepted", Boolean(), nullable=False)

    # password.create(users)
    accepted.create(friends)
    pass
