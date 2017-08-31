from sqlalchemy import *
from migrate import *


def upgrade(migrate_engine):
    meta = MetaData(bind=migrate_engine)

    users = Table('users', meta, autoload=True)

    # users.c.password.drop()
    users.c.newsletter.drop()

    notifpref = Table('notification_preferences', meta, autoload=True)

    newsletter_email = Column("newsletter_email", Boolean(), nullable=True)

    newsletter_email.create(notifpref)
    pass


def downgrade(migrate_engine):
    meta = MetaData(bind=migrate_engine)

    # users.c.password.drop()
    users = Table('users', meta, autoload=True)
    newsletter = Column("newsletter", Boolean(), nullable=True)
    newsletter.create(users)

    notifpref = Table('notification_preferences', meta, autoload=True)

    notifpref.c.newsletter_email.drop()
    pass
