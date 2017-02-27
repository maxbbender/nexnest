from nexnest.application import db

from .base import Base

from datetime import datetime as dt

from sqlalchemy.orm import relationship

from sqlalchemy.schema import UniqueConstraint

from flask import flash

import os


# class PostReport(Base):
class GroupListing(Base):
    __tablename__ = 'group_listings'
    id = db.Column(db.Integer, primary_key=True)
    group_id = db.Column(db.Integer,
                         db.ForeignKey('groups.id'))
    listing_id = db.Column(db.Integer,
                           db.ForeignKey('listings.id'))

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

    securityDeposits = relationship('SecurityDeposit', backref='groupListing')

    date_created = db.Column(db.DateTime)

    all_leases_submitted = db.Column(db.Boolean)

    messages = relationship('GroupListingMessage', backref='groupListing')

    __table_args__ = (UniqueConstraint('group_id', 'listing_id', name='groupListing_constraint'),
                      )

    def __init__(
            self,
            group,
            listing,
    ):
        self.group_id = group.id
        self.listing_id = listing.id
        self.group = group
        self.listing = listing

        self.accepted = False
        self.completed = False
        self.group_show = True
        self.landlord_show = True
        self.all_leases_submitted = False

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

    def isViewableBy(self, user):
        if user in self.group.getUsers():
            return True
        elif user in self.listing.landLordsAsUsers():
            return True
        else:
            flash("Permissions Error", 'danger')
            return False

    def isEditableBy(self, user):
        if user in self.listing.landLordsAsUsers():
            return True
        else:
            flash("Permissions Error", 'danger')
            return False

    def hasLease(self):
        if os.path.exists('./nexnest/uploads/leases/groupListingLease%d.pdf' % self.id):
            return True

        return False

    def canChangeLease(self):
        if len(self.securityDeposits) > 0:
            flash(
                'Cannot change lease, security deposits have already been submitted', 'danger')
            return False

        return True
