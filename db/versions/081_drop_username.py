from sqlalchemy import *
from migrate import *



def upgrade(migrate_engine):
    meta = MetaData(bind=migrate_engine)

    # users = Table('users', meta, autoload=True)
    users = Table('users', meta, autoload=True)

    # users.c.password.drop()
    users.c.username.drop()

    # Make email unique
    UniqueConstraint(users.c.email, name='emailUnique').create()
    pass


def downgrade(migrate_engine):
    meta = MetaData(bind=migrate_engine)

    # users = Table('users', meta, autoload=True)
    users = Table('users', meta, autoload=True)

    # password = Column("password", String(128), nullable=False)
    username = Column('username', String(length=80))

    # password.create(users)
    username.create(users)

    # Make email unique
    UniqueConstraint(users.c.email, name='emailUnique').drop()
    pass
