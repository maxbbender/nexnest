from datetime import datetime as dt

from nexnest.application import db, session

from flask import flash

from .base import Base

from sqlalchemy import event
from sqlalchemy.orm import relationship

from nexnest.models.group_user import GroupUser


class Group(Base):
    __tablename__ = 'groups'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    leader_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    date_created = db.Column(db.DateTime)
    date_modified = db.Column(db.DateTime)
    users = relationship("GroupUser", back_populates='group')
    listings = relationship("GroupListing", back_populates='group')
    messages = relationship("GroupMessage", backref='group')
    tours = relationship("Tour", backref='group')
    house = relationship("House", backref='group')
    favorites = relationship("GroupListingFavorite", backref='group')

    def __init__(
            self,
            name,
            leader,
            start_date,
            end_date
    ):
        self.start_date = start_date
        self.end_date = end_date
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

    @property
    def serialize(self):
        return {
            'leader': self.leader.shortSerialize(),
            'id': self.id,
            'name': self.name,
            'startDate': self.start_date,
            'endDate': self.end_date,
            'url': '/group/view/%d' % self.id
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
        for idx, groupUser in enumerate(self.users):
            if groupUser.accepted:
                if groupUser.user.id == self.leader_id and not leaderFound:
                    leaderFound = True

                    # If this is the first time through don't do anything
                    if idx > 0:
                        tempUser = acceptedUsers[0]
                        acceptedUsers[0] = groupUser.user
                        acceptedUsers.append(tempUser)
                        continue
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
