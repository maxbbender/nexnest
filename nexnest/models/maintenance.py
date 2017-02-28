from datetime import datetime as dt

from nexnest.application import db

from .base import Base

from sqlalchemy import event
from sqlalchemy.orm import relationship

from flask import flash


# class PostReport(Base):
class Maintenance(Base):
    __tablename__ = 'maintenances'
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String(10))
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

    def isEditableBy(self, user):
        if user in self.house.listing.landLordsAsUsers():
            return True

        flash('Permissions Error', 'warning')
        return False


def update_date_modified(mapper, connection, target):
    # 'target' is the inserted object
    target.date_modified = dt.now().isoformat()  # Update Date Modified


event.listen(Maintenance, 'before_update', update_date_modified)
