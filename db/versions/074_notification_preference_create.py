from migrate import *
from sqlalchemy import *

meta = MetaData()
# Column('XXXX', String(120)),
notificationPreference = Table('notification_preferences', meta,
                               Column('id', Integer(),
                                      primary_key=True, nullable=False),
                               Column('user_id', Integer()),
                               Column('date_created', DateTime()),
                               Column('date_modified', DateTime()),
                               Column('direct_message_notification', Boolean()),
                               Column('direct_message_email', Boolean()),
                               Column('tour_message_notification', Boolean()),
                               Column('tour_message_email', Boolean()),
                               Column('tour_time_notification', Boolean()),
                               Column('tour_time_email', Boolean()),
                               Column('group_message_notification', Boolean()),
                               Column('group_message_email', Boolean()),
                               Column('house_message_notification', Boolean()),
                               Column('house_message_email', Boolean()),
                               Column('tour_confirmed_notification', Boolean()),
                               Column('tour_confirmed_email', Boolean()),
                               Column('maintenance_notification', Boolean()),
                               Column('maintenance_email', Boolean()),
                               Column('maintenance_inProgress_notification', Boolean()),
                               Column('maintenance_inProgress_email', Boolean()),
                               Column('maintenance_completed_notification', Boolean()),
                               Column('maintenance_completed_email', Boolean()),
                               Column('maintenance_message_notification', Boolean()),
                               Column('maintenance_message_email', Boolean()),
                               Column('rent_due_notification', Boolean()),
                               Column('rent_due_email', Boolean()),
                               Column('rent_paid_notification', Boolean()),
                               Column('rent_paid_email', Boolean()),
                               Column('group_user_notification', Boolean()),
                               Column('group_user_email', Boolean()),
                               Column('group_listing_notification', Boolean()),
                               Column('group_listing_email', Boolean()),
                               Column('house_notification', Boolean()),
                               Column('house_email', Boolean()),
                               Column('tour_denied_notification', Boolean()),
                               Column('tour_denied_email', Boolean()),
                               Column('tour_create_notification', Boolean()),
                               Column('tour_create_email', Boolean()),
                               Column('group_listing_accept_notification', Boolean()),
                               Column('group_listing_accept_email', Boolean()),
                               Column('group_listing_deny_notification', Boolean()),
                               Column('group_listing_deny_email', Boolean()),
                               Column('group_user_completed_notification', Boolean()),
                               Column('group_user_completed_email', Boolean()),
                               Column('group_listing_favorite_notification', Boolean()),
                               Column('group_listing_favorite_email', Boolean()))

# Column('group_listing_completed_notification', Boolean()),
# Column('group_listing_completed_email', Boolean())


def upgrade(migrate_engine):
    meta.bind = migrate_engine
    notificationPreference.create()

    # users = Table('users', meta, autoload=True)
    # ForeignKeyConstraint(
    #     columns=[notificationPreference.c.user_id],
    #     refcolumns=[users.c.id]).create()
    pass


def downgrade(migrate_engine):
    meta.bind = migrate_engine

    # users = Table('users', meta, autoload=True)
    # ForeignKeyConstraint(
    #     columns=[notificationPreference.c.user_id],
    #     refcolumns=[users.c.id]).drop()

    notificationPreference.drop()
    pass
