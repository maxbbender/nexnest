from datetime import datetime as dt

from nexnest import db

from .base import Base

from sqlalchemy import event


# class PostReport(Base):
class GroupListing(Base):
    __tablename__ = 'group_users'
    group_id = db.Column(db.Integer,
                         primary_key=True,
                         db.ForiegnKey('groups.id'))
    listing_id = db.Column(db.Integer,
                           primary_key=True,
                           db.ForiegnKey('listings.id'))

    def __init__(
            self,
            group,
            listing
    ):
        self.group = group
        self.listing = listing

    def __repr__(self):
        return '<GroupListing ~ Group %r | Listing %r>' % \
            (self.group_id, self.listing_id)
