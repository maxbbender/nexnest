from nexnest.application import db

from .base import Base


# class PostReport(Base):
class GroupListing(Base):
    __tablename__ = 'group_listings'
    group_id = db.Column(db.Integer,
                         db.ForeignKey('groups.id'),
                         primary_key=True)
    listing_id = db.Column(db.Integer,
                           db.ForeignKey('listings.id'),
                           primary_key=True)

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
