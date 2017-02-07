from datetime import datetime as dt

from nexnest.application import db

from .base import Base

from sqlalchemy import event
from sqlalchemy.orm import relationship


# class PostReport(Base):
class House(Base):
    __tablename__ = 'houses'
    id = db.Column(db.Integer, primary_key=True)
    listing_id = db.Column(db.Integer, db.ForeignKey('listings.id'))
    group_id = db.Column(db.Integer, db.ForeignKey('groups.id'))
    date_created = db.Column(db.DateTime)
    date_modified = db.Column(db.DateTime)
    messages = relationship("HouseMessage", backref='house')

    def __init__(
            self,
            listing,
            group
    ):
        self.listing_id = listing.id
        self.group_id = group.id

        # Default Values
        now = dt.now().isoformat()  # Current Time to Insert into Datamodels
        self.date_created = now
        self.date_modified = now

    def __repr__(self):
        return '<House %r>' % self.id

    def isViewableBy(self, user):
        if user in self.group.acceptedUsers:
            return True

        return False


def update_date_modified(mapper, connection, target):
    # 'target' is the inserted object
    target.date_modified = dt.now().isoformat()  # Update Date Modified


event.listen(House, 'before_update', update_date_modified)
