from datetime import datetime as dt
import re

from nexnest import db

from flask import flash

from pprint import pprint

from .base import Base

from sqlalchemy import event
from sqlalchemy.orm import relationship

from nexnest.models.group_user import GroupUser
from nexnest.models.security_deposit import SecurityDeposit

session = db.session


class Group(Base):
    __tablename__ = 'groups'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    leader_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    target_time_period = db.Column(db.Text)
    # start_date = db.Column(db.Date)
    # end_date = db.Column(db.Date)
    date_created = db.Column(db.DateTime)
    date_modified = db.Column(db.DateTime)
    users = relationship("GroupUser", back_populates='group')
    listings = relationship("GroupListing", back_populates='group')
    messages = relationship("GroupMessage", backref='group')
    tours = relationship("Tour", backref='group')
    house = relationship("House", backref='group')
    favorites = relationship("GroupListingFavorite", backref='group')
    reports = relationship("ReportGroup", backref='group')
    emailInvites = relationship('GroupEmail', backref='group')

    def __init__(
            self,
            name,
            leader,
            target_time_period
            # start_date,
            # end_date
    ):
        # self.start_date = start_date
        # self.end_date = end_date
        self.target_time_period = target_time_period
        self.name = name

        self.leader = leader
        self.leader_id = leader.id

        # Default Values
        now = dt.now().isoformat()  # Current Time to Insert into Datamodels
        self.date_created = now
        self.date_modified = now

        # Group User
        newGU = GroupUser(group=self, user=leader)
        newGU.accepted = True

        session.add(newGU)
        session.commit()

    def __repr__(self):
        return '<Group %r - %r>' % (self.id, self.name)

    @property
    def serialize(self, groupListingID=None):
        group_users = []
        for user in self.acceptedUsers:
            group_users.append(user.shortSerialize)

        return {
            'leader': self.leader.shortSerialize,
            'id': self.id,
            'name': self.name,
            'targetTimePeriod': self.target_time_period,
            'url': '/group/view/%d' % self.id,
            'users': group_users,
            'userCount': len(group_users)
        }

    @property
    def unAcceptedUsers(self):
        unAcceptedUsers = []
        for groupUser in self.users:
            if not groupUser.accepted and groupUser.show:
                unAcceptedUsers.append(groupUser.user)

        return unAcceptedUsers

    @property
    def acceptedUsers(self):
        leaderFound = False
        acceptedUsers = []
        # print("Accepted Users for Group %r" % self)
        for idx, groupUser in enumerate(self.users):
            if groupUser.accepted:
                # print("Looking at user %r" % groupUser.user)
                if groupUser.user.id == self.leader_id and not leaderFound:
                    # print("Found Leader %r" % groupUser.user)
                    # pprint("Current List %r" % acceptedUsers)
                    leaderFound = True

                    # If this is the first time through don't do anything
                    if idx > 0:
                        tempUser = acceptedUsers[0]
                        acceptedUsers[0] = groupUser.user
                        acceptedUsers.append(tempUser)
                        continue
                    else:
                        acceptedUsers.append(groupUser.user)
                    # pprint("After List %r" % acceptedUsers)
                else:
                    acceptedUsers.append(groupUser.user)

        return acceptedUsers

    @property
    def housingRequests(self):
        housingRequests = []
        for groupListing in self.listings:
            if groupListing.group_show:
                housingRequests.append(groupListing)
        return housingRequests

    @property
    def hasAcceptedHouseRequest(self):
        for groupListing in self.listings:
            if groupListing.accepted:
                return True

        return False

    @property
    def humanTimePeriod(self):
        schoolYearPattern = re.compile(r"((\d{4})-(\d{4}))")
        schoolYear = schoolYearPattern.match(self.target_time_period)

        if schoolYear:
            firstYear = schoolYear.group(2)
            secondYear = schoolYear.group(3)
            return 'Fall %s - Spring %s' % (firstYear, secondYear)
        else:
            return 'Summer %s' % self.target_time_period

    def addUserToGroup(self, user):
        # First we want to check how many users are a part
        # of the group already. Max users 6
        num_users = session.query(GroupUser).filter_by(
            group_id=self.id).count()

        if num_users < 6:
            newGroupUser = GroupUser(self, user)
            session.add(newGroupUser)
            session.commit()
        else:
            flash("Group Size Limit Reached")

    def removeUser(self, user):
        user = session.query(GroupUser).filter_by(group_id=self.id, user_id=user.id).first()
        session.delete(user)
        session.commit()
        return True

    def getUsers(self):
        users = []
        for groupUser in self.users:
            users.append(groupUser.user)

        return users

    def isViewableBy(self, user, toFlash=True):
        if user in self.acceptedUsers:
            return True
        elif toFlash:
            flash("You do not have permissions to view this Group", 'warning')
        return False

    def isEditableBy(self, user, toFlash=True):
        if user.id == self.leader_id:
            return True
        elif toFlash:
            flash("You do not permissions to modify this group", 'warning')
        return False

    def hasTourForListing(self, listing):
        for tour in self.tours:
            if tour.listing.id == listing.id:
                return True

        return False

    def displayedFavorites(self):
        favorites = []
        for favorite in self.favorites:
            if favorite.show:
                favorites.append(favorite)

        return favorites

    def invalidateOpenInvitations(self):
        for groupUser in self.users:
            if not groupUser.accepted and groupUser.show:
                groupUser.show = False

        session.commit()


def update_date_modified(mapper, connection, target):  # pylint: disable=unused-argument
    # 'target' is the inserted object
    target.date_modified = dt.now().isoformat()  # Update Date Modified


event.listen(Group, 'before_update', update_date_modified)
