from sqlalchemy import *
from migrate import *


def upgrade(migrate_engine):
    meta = MetaData(bind=migrate_engine)

    # users = Table('users', meta, autoload=True)
    AAAA = Table('AAAA', meta, autoload=True)

    # users.c.password.drop()
    AAAA.c.XXXX.drop()
    pass


def downgrade(migrate_engine):
    meta = MetaData(bind=migrate_engine)

    # users = Table('users', meta, autoload=True)
    AAAA = Table('XXXX', meta, autoload=True)

    # password = Column("password", String(128), nullable=False)
    BBBB = Column("XXXX", String(128))
    CCCC = Column("XXXX", String(128))

    # password.create(users)
    BBBB.create(AAAA)
    CCCC.create(AAAA)
    pass
