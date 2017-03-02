from datetime import datetime as dt

from sqlalchemy import event
from sqlalchemy.orm import relationship

from nexnest.application import db

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

        # Default Values
        now = dt.now().isoformat()  # Current Time to Insert into Datamodels
        self.date_created = now
        self.date_modified = now

    def __repr__(self):
        return '<Tour %r>' % self.id

    def isViewableBy(self, user):
        if user in self.group.getUsers() or user in self.listing.landLordsAsUsers():
            return True

        return False

    def isEditableBy(self, user):
        if user == self.group.leader or user in self.listing.landLordsAsUsers():
            return True

        return False


def update_date_modified(mapper, connection, target):  # pylint: disable=unused-argument
    # 'target' is the inserted object
    target.date_modified = dt.now().isoformat()  # Update Date Modified


event.listen(Tour, 'before_update', update_date_modified)
