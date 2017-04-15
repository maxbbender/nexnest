from sqlalchemy import *
from migrate import *


def downgrade(migrate_engine):
    meta = MetaData(bind=migrate_engine)

    # users = Table('users', meta, autoload=True)
    groups = Table('groups', meta, autoload=True)

    # users.c.password.drop()
    # groups.c.start_date.drop()
    # groups.c.end_date.drop()
    groups.c.target_time_period.drop()
    pass


def upgrade(migrate_engine):
    meta = MetaData(bind=migrate_engine)

    # users = Table('users', meta, autoload=True)
    groups = Table('groups', meta, autoload=True)

    # password = Column("password", String(128), nullable=False)
    # start_date = Column("start_date", Date())
    # end_date = Column("end_date", Date())
    target_time_period = Column('target_time_period', Text())

    # password.create(users)
    # start_date.create(groups)
    # end_date.create(groups)
    target_time_period.create(groups)
    pass
