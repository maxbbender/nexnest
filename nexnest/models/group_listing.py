import os

from datetime import datetime as dt

from sqlalchemy.orm import relationship
from sqlalchemy.schema import UniqueConstraint

from flask import flash

from nexnest.application import db, session
from nexnest.models.notification import Notification

from .base import Base


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
        return '<GroupListing %r ~ Group %r | Listing %r>' % \
            (self.id, self.group_id, self.listing_id)

    @property
    def status(self):
        if self.completed:
            return 'Completed'
        elif self.accepted:
            return 'Accepted'
        else:
            return 'Not Accepted'

    @property
    def serialize(self):
        group = self.group.serialize

        for user in group['users']:
            # Find the security deposit record
            for deposit in self.securityDeposits:
                if deposit.user_id == user['id']:
                    if deposit.completed:
                        user['securityDepositPaid'] = True
                    else:
                        user['securityDepositPaid'] = False
                    break

        groupListing = {
            'id': self.id,
            'accepted': self.accepted,
            'completed': self.completed,
            'url': '/houseRequest/view/%d' % self.id,
            'group': group,
            'leasesCollected': self.all_leases_submitted
        }

        if self.firstMessage is not None:
            groupListing['message'] = self.firstMessage.content

        return groupListing

    def isViewableBy(self, user, toFlash=True):
        if user in self.group.getUsers():
            return True
        elif user in self.listing.landLordsAsUsers():
            return True
        else:
            if toFlash:
                flash("Permissions Error", 'danger')
            return False

    def isEditableBy(self, user, toFlash=True):
        if user in self.listing.landLordsAsUsers():
            return True
        else:
            if toFlash:
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

    @property
    def firstMessage(self):
        firstMessage = None
        for message in self.messages:
            if firstMessage is None:
                firstMessage = message
                continue

            if message.date_created < firstMessage.date_created:
                firstMessage = message
                continue

        return firstMessage

    @property
    def numSecurityDepositsPaid(self):
        if not self.accepted:
            return 0

        numPaid = 0
        for securityDeposit in self.securityDeposits:
            if securityDeposit.completed:
                numPaid += 1

        return numPaid

    @property
    def allSecurityDepositsPaid(self):
        for deposit in self.securityDeposits:
            if not deposit.completed:
                return False

        return True

    def genNotifications(self):
        for landlord in self.listing.landLordsAsUsers():

            newNotif = Notification(notif_type='group_listing',
                                    target_model_id=self.id,
                                    target_user=landlord)
            session.add(newNotif)
            session.commit()

    def genAcceptedNotifications(self):
        for user in self.group.acceptedUsers:
            newNotif = Notification(notif_type='group_listing_accept',
                                    target_user=user,
                                    target_model_id=self.id)
            session.add(newNotif)
            session.commit()

    def undoAcceptedNotifications(self):
        session.query(Notification) \
            .filter_by(notif_type='group_listing_accept',
                       target_model_id=self.id) \
            .delete()

        session.commit()

    def genDeniedNotifications(self):
        for user in self.group.acceptedUsers:
            newNotif = Notification(notif_type='group_listing_denied',
                                    target_user=user,
                                    target_model_id=self.id)
            session.add(newNotif)
            session.commit()

    def undoDeniedNotifications(self):
        session.query(Notification) \
            .filter_by(notif_type='group_listing_denied',
                       target_model_id=self.id) \
            .delete()

        session.commit()

    def genCompletedNotifications(self):
        for user in self.group.acceptedUsers:
            newNotif = Notification(notif_type='group_listing_completed',
                                    target_user=user,
                                    target_model_id=self.id)
            session.add(newNotif)
            session.commit()

        for landlord in self.listing.landLordsAsUsers():
            newNotif = Notification(notif_type='group_listing_completed',
                                    target_user=landlord,
                                    target_model_id=self.id)
            session.add(newNotif)
            session.commit()

    def undoCompletedNotifications(self):
        session.query(Notification) \
            .filter_by(notif_type='group_listing_completed',
                       target_model_id=self.id) \
            .delete()

        session.commit()
