from sqlalchemy import event
from sqlalchemy.orm import relationship

from datetime import datetime as dt

from nexnest.application import db

from nexnest.models.base import Base
# _notification = db.Column(db.Boolean)
# _email = db.Column(db.Boolean)


class NotificationPreference(Base):
    __tablename__ = 'notification_preferences'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('users.id'))
    date_created = db.Column(db.DateTime)
    date_modified = db.Column(db.DateTime)

    direct_message_notification = db.Column(db.Boolean)
    direct_message_email = db.Column(db.Boolean)

    tour_message_notification = db.Column(db.Boolean)  # D
    tour_message_email = db.Column(db.Boolean)         # D

    tour_time_notification = db.Column(db.Boolean)  # D
    tour_time_email = db.Column(db.Boolean)  # D

    group_message_notification = db.Column(db.Boolean)  # D
    group_message_email = db.Column(db.Boolean)  # D

    house_message_notification = db.Column(db.Boolean)  # D
    house_message_email = db.Column(db.Boolean)  # D

    tour_confirmed_notification = db.Column(db.Boolean)  # D
    tour_confirmed_email = db.Column(db.Boolean)  # D

    tour_denied_notification = db.Column(db.Boolean)  # D
    tour_denied_email = db.Column(db.Boolean)  # D

    maintenance_notification = db.Column(db.Boolean) # D
    maintenance_email = db.Column(db.Boolean) # D

    maintenance_inProgress_notification = db.Column(db.Boolean) # D
    maintenance_inProgress_email = db.Column(db.Boolean) # D

    maintenance_completed_notification = db.Column(db.Boolean) # D
    maintenance_completed_email = db.Column(db.Boolean) # D

    maintenance_message_notification = db.Column(db.Boolean) # D
    maintenance_message_email = db.Column(db.Boolean) # D

    rent_due_notification = db.Column(db.Boolean)
    rent_due_email = db.Column(db.Boolean)

    rent_paid_notification = db.Column(db.Boolean)
    rent_paid_email = db.Column(db.Boolean)

    group_user_notification = db.Column(db.Boolean)
    group_user_email = db.Column(db.Boolean)

    group_listing_notification = db.Column(db.Boolean) # D
    group_listing_email = db.Column(db.Boolean) # D

    group_listing_accept_notification = db.Column(db.Boolean) # D
    group_listing_accept_email = db.Column(db.Boolean) # D

    group_listing_deny_notification = db.Column(db.Boolean) # D
    group_listing_deny_email = db.Column(db.Boolean) # D

    group_listing_completed_notification = db.Column(db.Boolean) # D
    group_listing_completed_email = db.Column(db.Boolean) # D

    house_notification = db.Column(db.Boolean)
    house_email = db.Column(db.Boolean)

    tour_create_notification = db.Column(db.Boolean)  # D
    tour_create_email = db.Column(db.Boolean)  # D

    user = relationship('User', back_populates='notificationPreference')

    def __init__(
            self,
            user
    ):

        self.user = user
        # Default Values
        now = dt.now().isoformat()  # Current Time to Insert into Datamodels
        self.date_created = now
        self.date_modified = now

        # Notification Preference Defaults
        self.direct_message_notification = True
        self.direct_message_notification = False

        self.tour_message_notification = True
        self.tour_message_email = False

        self.tour_time_notification = True
        self.tour_time_email = False

        self.group_message_notification = True
        self.group_message_email = False

        self.house_message_notification = True
        self.house_message_email = False

        self.tour_confirmed_notification = True
        self.tour_confirmed_email = False

        self.maintenance_notification = True
        self.maintenance_email = True

        self.maintenance_inProgress_notification = True
        self.maintenance_inProgress_email = False

        self.maintenance_completed_notification = True
        self.maintenance_completed_email = False

        self.maintenance_message_notification = True
        self.maintenance_message_email = False

        self.rent_due_notification = True
        self.rent_due_email = True

        self.rent_paid_notification = True
        self.rent_paid_email = False

        self.group_user_notification = True
        self.group_user_email = True

        self.group_listing_notification = True
        self.group_listing_email = True

        self.house_notification = True
        self.house_email = True

        self.tour_denied_notification = True
        self.tour_denied_email = False

        self.tour_create_notification = True
        self.tour_create_email = True

        self.group_listing_accept_notification = True
        self.group_listing_accept_email = False

        self.group_listing_deny_notification = True
        self.group_listing_deny_email = True

        self.group_listing_completed_notification = True
        self.group_listing_completed_email = False

    def __repr__(self):
        return '<NotificationPreferences %d | User %r>' % (self.id, self.user)


def update_date_modified(mapper, connection, target):
    # 'target' is the inserted object
    target.date_modified = dt.now().isoformat()  # Update Date Modified


event.listen(NotificationPreference, 'before_update', update_date_modified)
