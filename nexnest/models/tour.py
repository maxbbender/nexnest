from datetime import datetime as dt

from nexnest.application import db

from .base import Base

from sqlalchemy import event


# class PostReport(Base):
class Tour(Base):
    __tablename__ = 'tours'
    id = db.Column(db.Integer, primary_key=True)
    listing_id = db.Column(db.Integer, db.ForeignKey('listings.id'))
    group_id = db.Column(db.Integer, db.ForeignKey('groups.id'))
    time_requested = db.Column(db.DateTime)
    description = db.Column(db.Text)
    date_created = db.Column(db.DateTime)
    date_modified = db.Column(db.DateTime)

    def __init__(
            self,
            listing,
            group,
            time_requested,
            description
    ):
        self.listing = listing
        self.group = group

        self.time_requested = time_requested
        self.description = description

        # Default Values
        now = dt.now().isoformat()  # Current Time to Insert into Datamodels
        self.date_created = now
        self.date_modified = now

    def __repr__(self):
        return '<Tour %r>' % self.id


def update_date_modified(mapper, connection, target):
    # 'target' is the inserted object
    target.date_modified = dt.now().isoformat()  # Update Date Modified


event.listen(Tour, 'before_update', update_date_modified)
