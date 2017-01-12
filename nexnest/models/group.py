from datetime import datetime as dt

from nexnest.application import db, session

from flask import flash

from .base import Base

from sqlalchemy import event
from sqlalchemy.orm import relationship

from .group_user import GroupUser
# from nexnest.models.user import User


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
        self.leader_id = leader.id

        # Default Values
        now = dt.now().isoformat()  # Current Time to Insert into Datamodels
        self.date_created = now
        self.date_modified = now

    def __repr__(self):
        return '<Group %r>' % self.name

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

    # @property
    # def acceptedGroupUsers(self):
    #     acceptedUsers = []
    #     acceptedGroupUsers = session.query(GroupUser).filter_by(
    #         group_id=self.id, accepted=True).all()

    #     for groupUser in acceptedGroupUsers:
    #         acceptedUsers.append(session.query(
    #             'User').filter_by(id=groupUser.user_id).first())

    #     return acceptedUsers


def update_date_modified(mapper, connection, target):
    # 'target' is the inserted object
    target.date_modified = dt.now().isoformat()  # Update Date Modified


event.listen(Group, 'before_update', update_date_modified)
