from sqlalchemy import *
from migrate import *


def upgrade(migrate_engine):
    meta = MetaData(bind=migrate_engine)

    # users = Table('users', meta, autoload=True)
    tours = Table('tours', meta, autoload=True)

    # users.c.password.drop()
    tours.c.description.drop()
    pass


def downgrade(migrate_engine):
    meta = MetaData(bind=migrate_engine)

    # users = Table('users', meta, autoload=True)
    tours = Table('tours', meta, autoload=True)

    # password = Column("password", String(128), nullable=False)
    description = Column("description", Text())

    # password.create(users)
    description.create(tours)
    pass
