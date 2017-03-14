from datetime import datetime as dt

from sqlalchemy import event
from sqlalchemy.orm import relationship

from flask import flash

from nexnest.application import db, session
from nexnest.models.notification import Notification

from .base import Base


class Tour(Base):
    __tablename__ = 'tours'
    id = db.Column(db.Integer, primary_key=True)
    listing_id = db.Column(db.Integer, db.ForeignKey('listings.id'))
    group_id = db.Column(db.Integer, db.ForeignKey('groups.id'))
    time_requested = db.Column(db.DateTime)
    date_created = db.Column(db.DateTime)
    date_modified = db.Column(db.DateTime)
    tour_confirmed = db.Column(db.Boolean)
    last_requested = db.Column(db.String(8))
    declined = db.Column(db.Boolean)
    messages = relationship('TourMessage', backref='tour')

    def __init__(
            self,
            listing,
            group,
            time_requested
    ):
        self.listing = listing
        self.group = group

        self.time_requested = time_requested

        self.last_requested = 'group'
        self.tour_confirmed = False
        self.declined = False

        # Default Values
        now = dt.now().isoformat()  # Current Time to Insert into Datamodels
        self.date_created = now
        self.date_modified = now

    def __repr__(self):
        return '<Tour %r>' % self.id

    def isViewableBy(self, user, toFlash=True):
        if user in self.group.getUsers() or user in self.listing.landLordsAsUsers():
            return True
        elif toFlash:
            flash("Permissions Error")

        return False

    def isEditableBy(self, user, toFlash=True):
        if user == self.group.leader or user in self.listing.landLordsAsUsers():
            return True
        elif toFlash:
            flash("Permissions Error")

        return False

    def genNotifications(self):
        for landlord in self.listing.landLordsAsUsers():
            newNotif = Notification(notif_type='tour',
                                    target_user=landlord,
                                    target_model_id=self.id)
            session.add(newNotif)
            session.commit()

    def genConfirmNotifications(self):
        for user in self.group.acceptedUsers:
            newNotif = Notification(notif_type='tour_confirmed',
                                    target_user=user,
                                    target_model_id=self.id)
            session.add(newNotif)
            session.commit()

    def undoConfirmNotifications(self):
        session.query(Notification) \
            .filter_by(notif_type='tour_confirmed',
                       target_model_id=self.id) \
            .delete()
        session.commit()

    def genTimeChangeNotifications(self):
        if self.last_requested == 'landlord':
            for user in self.group.acceptedUsers:
                newNotif = Notification(notif_type='new_tour_time',
                                        target_user=user,
                                        target_model_id=self.id)
                session.add(newNotif)
                session.commit()
        else:
            for user in self.listing.landLordsAsUsers():
                newNotif = Notification(notif_type='new_tour_time',
                                        target_user=user,
                                        target_model_id=self.id)
                session.add(newNotif)
                session.commit()

    def undoTimeChangeNotifications(self):
        session.query(Notification) \
            .filter_by(notif_type='new_tour_time',
                       target_model_id=self.id) \
            .delete()
        session.commit()

    def genDeniedNotifications(self):
        for user in self.group.acceptedUsers:
            newNotif = Notification(notif_type='tour_denied',
                                    target_user=user,
                                    target_model_id=self.id)
            session.add(newNotif)
            session.commit()

    def undoDeniedNotifications(self):
        session.query(Notification) \
            .filter_by(notif_type='tour_denied',
                       target_model_id=self.id) \
            .delete()
        session.commit()


def update_date_modified(mapper, connection, target):  # pylint: disable=unused-argument
    # 'target' is the inserted object
    target.date_modified = dt.now().isoformat()  # Update Date Modified


event.listen(Tour, 'before_update', update_date_modified)
