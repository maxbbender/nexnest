from sqlalchemy import *
from migrate import *


def downgrade(migrate_engine):
    meta = MetaData(bind=migrate_engine)

    # users = Table('users', meta, autoload=True)
    messages = Table('messages', meta, autoload=True)

    # users.c.password.drop()
    messages.c.type.drop()
    pass


def upgrade(migrate_engine):
    meta = MetaData(bind=migrate_engine)

    # users = Table('users', meta, autoload=True)
    messages = Table('messages', meta, autoload=True)

    # password = Column("password", String(128), nullable=False)
    type = Column("type", String(50))

    type.create(messages)
    pass
