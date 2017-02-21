from datetime import datetime as dt

from nexnest.application import db

from .base import Base

from sqlalchemy import event


# class PostReport(Base):
class Notification(Base):
    __tablename__ = 'notifications'
    id = db.Column(db.Integer, primary_key=True)
    target_user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    target_model_id = db.Column(db.Integer)
    viewed = db.Column(db.Boolean)
    date_created = db.Column(db.DateTime)
    date_modified = db.Column(db.DateTime)

    # Notification Type: Can be the following values
    # | direct_message        | friend        | group_user       | group_listing
    # | group_listing_message | group_message | house            | house_message
    # | maintenance_message   | maintenance   | platform_report  | report_group
    # | report_landlord       | report_listing| security_deposit | tour
    # | tour_message          | rent_reminder | new_tour_time    |
    type = db.Column(db.String(128))

    def __init__(
            self,
            target_user,
            target_model_id,
            type
    ):
        self.target_user_id = target_user.id
        self.type = type
        self.viewed = False

        # Default Values
        now = dt.now().isoformat()  # Current Time to Insert into Datamodels
        self.date_created = now
        self.date_modified = now

    def __repr__(self):
        return '<Notification %r>' % self.id


def update_date_modified(mapper, connection, target):
    # 'target' is the inserted object
    target.date_modified = dt.now().isoformat()  # Update Date Modified


event.listen(Notification, 'before_update', update_date_modified)
