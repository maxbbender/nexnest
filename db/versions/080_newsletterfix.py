from sqlalchemy import *
from migrate import *


def upgrade(migrate_engine):
    meta = MetaData(bind=migrate_engine)

    notifpref = Table('notification_preferences', meta, autoload=True)

    newsletter_email = Column("newsletter_email", Boolean(), nullable=True)

    newsletter_email.create(notifpref)
    pass


def downgrade(migrate_engine):
    meta = MetaData(bind=migrate_engine)

    notifpref = Table('notification_preferences', meta, autoload=True)

    notifpref.c.newsletter_email.drop()
    pass
