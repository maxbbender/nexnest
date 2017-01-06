from sqlalchemy import *
from migrate import *


def upgrade(migrate_engine):
    meta = MetaData(bind=migrate_engine)

    # users = Table('users', meta, autoload=True)
    users = Table('users', meta, autoload=True)

    # users.c.password.drop()
    users.c.role.drop()
    pass


def downgrade(migrate_engine):
    meta = MetaData(bind=migrate_engine)

    # users = Table('users', meta, autoload=True)
    users = Table('users', meta, autoload=True)

    # password = Column("password", String(128), nullable=False)
    role = Column('role', String(length=10))

    # password.create(users)
    users.create(role)
    pass
