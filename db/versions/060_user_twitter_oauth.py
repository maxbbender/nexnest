from sqlalchemy import *
from migrate import *


def downgrade(migrate_engine):
    meta = MetaData(bind=migrate_engine)

    users = Table('users', meta, autoload=True)

    # users.c.password.drop()
    users.c.social_id.drop()
    pass


def upgrade(migrate_engine):
    meta = MetaData(bind=migrate_engine)

    users = Table('users', meta, autoload=True)

    # password = Column("password", String(128), nullable=False)
    social_id = Column("social_id", Text())

    # password.create(users)
    social_id.create(users)
    pass
