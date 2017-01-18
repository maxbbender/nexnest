from nexnest.application import db

from .base import Base

from datetime import datetime as dt

from sqlalchemy.orm import relationship


# class PostReport(Base):
class GroupListing(Base):
    __tablename__ = 'group_listings'
    group_id = db.Column(db.Integer,
                         db.ForeignKey('groups.id'),
                         primary_key=True)
    listing_id = db.Column(db.Integer,
                           db.ForeignKey('listings.id'),
                           primary_key=True)
    req_description = db.Column(db.Text)

    # This is for when a group has been accepted and the process
    # of putting in the down payment and signing the lease is
    # still underway
    accepted = db.Column(db.Boolean)

    # This is for when a group has been accepted and the process
    # is finished. All leases signed and they are living in the
    # house.
    completed = db.Column(db.Boolean)

    # Whether or not to show the group_listing for the User suggested listings
    # page
    group_show = db.Column(db.Boolean)
    landlord_show = db.Column(db.Boolean)

    group = relationship("Group", back_populates="listings")
    listing = relationship("Listing", back_populates='groups')

    date_created = db.Column(db.DateTime)

    def __init__(
            self,
            group,
            listing,
            req_description
    ):
        self.group_id = group.id
        self.listing_id = listing.id
        self.group = group
        self.listing = listing
        self.req_description = req_description

        self.accepted = False
        self.completed = False
        self.group_show = True
        self.landlord_show = True

        # Default Values
        now = dt.now().isoformat()  # Current Time to Insert into Datamodels
        self.date_created = now

    def __repr__(self):
        return '<GroupListing ~ Group %r | Listing %r>' % \
            (self.group_id, self.listing_id)

    @property
    def status(self):
        if self.completed:
            return 'Completed'
        elif self.accepted:
            return 'Accepted'
        else:
            return 'Not Accepted'
