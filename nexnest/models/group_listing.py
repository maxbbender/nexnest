from nexnest.application import db

from .base import Base

from datetime import datetime as dt


# class PostReport(Base):
class GroupListing(Base):
    __tablename__ = 'group_listings'
    group_id = db.Column(db.Integer,
                         db.ForeignKey('groups.id'),
                         primary_key=True)
    listing_id = db.Column(db.Integer,
                           db.ForeignKey('listings.id'),
                           primary_key=True)

    # This is for when a group has been accepted and the process
    # of putting in the down payment and signing the lease is
    # still underway
    accepted = db.Column(db.Boolean)

    # This is for when a group has been accepted and the process
    # is finished. All leases signed and they are living in the
    # house.
    completed = db.Column(db.Boolean)

    # Whether or not to show the group_listing for the Landlord
    # page
    show = db.Column(db.Boolean)

    date_created = db.Column(db.DateTime)

    def __init__(
            self,
            group,
            listing
    ):
        self.group = group
        self.listing = listing

        self.accepted = False
        self.completed = False
        self.show = True

        # Default Values
        now = dt.now().isoformat()  # Current Time to Insert into Datamodels
        self.date_created = now

    def __repr__(self):
        return '<GroupListing ~ Group %r | Listing %r>' % \
            (self.group_id, self.listing_id)
