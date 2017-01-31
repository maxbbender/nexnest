from sqlalchemy import *
from migrate import *


def downgrade(migrate_engine):
    meta = MetaData(bind=migrate_engine)

    users = Table('users', meta, autoload=True)

    # users.c.password.drop()
    users.c.twitter_token.drop()
    users.c.twitter_secret.drop()
    pass


def downgrade(migrate_engine):
    meta = MetaData(bind=migrate_engine)

    users = Table('users', meta, autoload=True)

    # password = Column("password", String(128), nullable=False)
    twitter_token = Column("twitter_token", Text())
    CCCC = Column("XXXX", String(128))

    # password.create(users)
    BBBB.create(AAAA)
    CCCC.create(AAAA)
    pass
