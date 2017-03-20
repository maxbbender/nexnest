# open | inprogress | completedfrom datetime import datetime as dt
from datetime import datetime as dt

from sqlalchemy import event
from sqlalchemy.orm import relationship

from flask import flash

from nexnest.application import db, session

from nexnest.models.base import Base
from nexnest.models.notification import Notification


class Maintenance(Base):
    __tablename__ = 'maintenances'
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String(10))  # open | inprogress | completed
    request_type = db.Column(db.String(20))
    details = db.Column(db.Text())
    house_id = db.Column(db.Integer, db.ForeignKey('houses.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    date_created = db.Column(db.DateTime)
    date_modified = db.Column(db.DateTime)
    messages = relationship('MaintenanceMessage', backref='maintenance')

    def __init__(
            self,
            request_type,
            details,
            house,
            user
    ):

        self.house_id = house.id
        self.details = details
        self.status = 'open'
        self.request_type = request_type
        self.user_id = user.id

        # Default Values
        now = dt.now().isoformat()  # Current Time to Insert into Datamodels
        self.date_created = now
        self.date_modified = now

    def __repr__(self):
        return '<Maintenance %r>' % self.id

    @property
    def serialize(self):
        return {
            'id': self.id,
            'status': self.status,
            'details': self.details,
            'requestType': self.humanRequestType,
            'date': self.date_created.strftime("%B %d, %Y"),
            'requestedBy': self.user.shortSerialize,
            'dateCompleted': self.date_modified.strftime("%B %d, %Y"),
            'url': '/house/maintenanceRequest/%d/view' % self.id
        }

    @property
    def humanRequestType(self):
        if self.request_type == 'heatingCooling':
            return 'Heating | Cooling'
        elif self.request_type == 'internet':
            return 'Internet'
        elif self.request_type == 'yardDriveway':
            return 'Yard | Driveway'
        elif self.request_type == 'appliance':
            return 'Appliance'
        elif self.request_type == 'plumbing':
            return 'Plumbing'
        elif self.request_type == 'electrical':
            return 'Electrical'
        elif self.request_type == 'furnishing':
            return 'Furnishing'
        elif self.request_type == 'other':
            return 'Other'

    def isEditableBy(self, user):
        if user in self.house.listing.landLordsAsUsers():
            return True

        flash('Permissions Error', 'warning')
        return False

    def genNotifications(self):
        for user in self.house.tenants:
            if user is not self.user:
                newNotif = Notification(notif_type='maintenance',
                                        target_model_id=self.id,
                                        target_user=user)
                session.add(newNotif)
                session.commit()

    def genInProgressNotifications(self):
        for user in self.house.tenants:
            newNotif = Notification(notif_type='maintenance_inprogress',
                                    target_model_id=self.id,
                                    target_user=user)
            session.add(newNotif)
            session.commit()

    def genCompletedNotifications(self):
        for user in self.house.tenants:
            newNotif = Notification(notif_type='maintenance_completed',
                                    target_model_id=self.id,
                                    target_user=user)
            session.add(newNotif)
            session.commit()

    def removeInProgressNotifications(self):
        # notifs = session.query(Notification).filter_by(notif_type='maintenance_inprogress',
        #                                                target_model_id=self.id)
        # session.delete(notifs)
        # session.commit()
        session.query(Notification).filter_by(notif_type='maintenance_inprogress',
                                              target_model_id=self.id) \
            .delete()

        session.commit()

    def removeCompletedNotifications(self):
        # notifs = session.query(Notification).filter_by(notif_type='maintenance_completed',
        #                                                target_model_id=self.id)
        # session.delete(notifs)
        # session.commit()
        session.query(Notification).filter_by(notif_type='maintenance_completed',
                                              target_model_id=self.id) \
            .delete()

        session.commit()


def update_date_modified(mapper, connection, target):  # pylint: disable=unused-argument
    # 'target' is the inserted object
    target.date_modified = dt.now().isoformat()  # Update Date Modified


event.listen(Maintenance, 'before_update', update_date_modified)
