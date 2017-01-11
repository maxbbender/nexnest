from datetime import datetime as dt

from nexnest.application import db

from .base import Base

from sqlalchemy import event


# class PostReport(Base):
class Maintenance(Base):
    __tablename__ = 'maintenances'
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String(10))
    request_type = db.Column(db.String(20))
    details = db.Column(db.Text())
    listing_id = db.Column(db.Integer, db.ForeignKey('listings.id'))
    date_created = db.Column(db.DateTime)
    date_modified = db.Column(db.DateTime)

    def __init__(
            self,
            request_type,
            details,
            listing
    ):

        self.listing_id = listing.id
        self.details = details
        self.status = 'open'
        self.request_type = request_type

        # Default Values
        now = dt.now().isoformat()  # Current Time to Insert into Datamodels
        self.date_created = now
        self.date_modified = now

    def __repr__(self):
        return '<Maintenance %r>' % self.id


def update_date_modified(mapper, connection, target):
    # 'target' is the inserted object
    target.date_modified = dt.now().isoformat()  # Update Date Modified


event.listen(Maintenance, 'before_update', update_date_modified)
