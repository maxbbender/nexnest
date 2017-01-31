from sqlalchemy import *
from migrate import *


def downgrade(migrate_engine):
    meta = MetaData(bind=migrate_engine)

    users = Table('users', meta, autoload=True)

    # users.c.password.drop()
    users.c.twitter_token.drop()
    users.c.twitter_secret.drop()
    pass


def upgrade(migrate_engine):
    meta = MetaData(bind=migrate_engine)

    users = Table('users', meta, autoload=True)

    # password = Column("password", String(128), nullable=False)
    twitter_token = Column("twitter_token", Text())
    twitter_secret = Column("twitter_secret", Text())

    # password.create(users)
    twitter_secret.create(users)
    twitter_token.create(users)
    pass
