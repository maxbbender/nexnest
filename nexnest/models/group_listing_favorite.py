from datetime import datetime as dt

from nexnest.application import db

from .base import Base


class GroupListingFavorite(Base):
    __tablename__ = 'group_listing_favorites'
    group_id = db.Column(db.Integer, db.ForeignKey('groups.id'), primary_key=True)
    listing_id = db.Column(db.Integer, db.ForeignKey('listings.id'), primary_key=True)
    date_created = db.Column(db.DateTime)

    def __init__(
            self,
            group,
            listing
    ):
        self.group_id = group.id
        self.listing_id = listing.id

        # Default Values
        now = dt.now().isoformat()  # Current Time to Insert into Datamodels
        self.date_created = now

    def __repr__(self):
        return '<GroupListingFavorite ~ Group %r | Listing %r>' % (self.group_id, self.listing_id)
