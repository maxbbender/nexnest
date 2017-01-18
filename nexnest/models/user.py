
from nexnest.application import db, session
from nexnest.utils.password import hash_password

from nexnest.models.group import Group
from nexnest.models.group_user import GroupUser
from nexnest.models.group_listing import GroupListing

from .base import Base
from .landlord import Landlord

from datetime import datetime as dt

from sqlalchemy.orm import relationship

from flask import flash


class User(Base):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(128), nullable=False)
    salt = db.Column(db.String(128), nullable=False)
    fname = db.Column(db.String(128))
    lname = db.Column(db.String(128))
    bio = db.Column(db.Text)
    role = db.Column(db.String(10))
    website = db.Column(db.String(128))
    location = db.Column(db.String(128))
    phone = db.Column(db.String(10))
    dob = db.Column(db.Date)
    profile_image = db.Column(db.String(128))
    date_created = db.Column(db.String(128), nullable=False)
    date_modified = db.Column(db.String(128), nullable=False)
    school_id = db.Column(db.Integer(), db.ForeignKey('schools.id'))
    active = db.Column(db.Boolean)
    sentDM = relationship('DirectMessage',
                          backref='source_user',
                          foreign_keys='[DirectMessage.source_user_id]')
    recievedDM = relationship('DirectMessage',
                              backref='target_user',
                              foreign_keys='[DirectMessage.target_user_id]')
    groups = relationship("GroupUser", back_populates='user')

    groupLeader = relationship("Group", backref='leader')
    groupMessages = relationship("GroupMessage", backref='user')

    def __init__(self,
                 email,
                 password,
                 fname,
                 lname,
                 school,
                 role=None,
                 bio=None,
                 website=None,
                 location=None,
                 phone=None,
                 dob=None,
                 profile_image=None,
                 ):

        self.school_id = school.id
        self.username = email.split("@")[0]
        self.email = email

        self.set_password(password)

        self.fname = fname
        self.lname = lname

        self.bio = bio
        self.website = website
        self.location = location
        self.phone = phone
        self.dob = dob

        if role is None:
            role = 'user'

        # if profile_image is None:
        #     image_num = format(randrange(1, 11), '03')

        #     self.profile_image = '/static/img/default{0}.jpg'.format(image_num)
        # else:
        #     self.profile_image = profile_image

        # Default Values
        now = dt.now().isoformat()  # Current Time to Insert into Datamodels
        self.date_created = now
        self.date_modified = now
        self.active = True

    def __repr__(self):
        return '<User %r>' % self.username

    def set_password(self, __password__):
        if __password__ == "":
            return self

        # Hash the password. SHA256
        hashedPassword = hash_password(__password__)

        # Split the password and the salt
        splitPassword = hashedPassword.split(":")

        self.password = splitPassword[0]  # Password
        self.salt = splitPassword[1]     # Salt

        return self

    @property
    def serialize(self):
        return {
            'id': self.id,
            'username': self.username,
            'fname': self.fname,
            'lname': self.lname
        }

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        try:
            return unicode(self.id)  # python 2
        except NameError:
            return str(self.id)  # python 3

    @property
    def accepted_groups(self):
        acceptedGroups = []
        for groupUser in self.groups:
            if groupUser.accepted:
                acceptedGroups.append(groupUser.group)

        return acceptedGroups

    @property
    def un_accepted_groups(self):
        unAcceptedGroups = []
        for groupUser in self.groups:
            if not groupUser.accepted and groupUser.show:
                unAcceptedGroups.append(groupUser.group)

        return unAcceptedGroups

    def accept_group_invite(self, group):
        group_user = session.query(GroupUser).filter_by(
            accepted=False,
            group_id=group.id,
            user_id=self.id).first()

        if group_user is not None:
            group_user.accepted = True
            session.commit()
            flash("Group invite accepted", 'info')
        else:
            flash("Unable to find record to accept")

    def decline_group_invite(self, group):
        group_user = session.query(GroupUser).filter_by(
            accepted=False,
            group_id=group.id,
            user_id=self.id).first()

        if group_user is not None:
            group_user.show = False
            session.commit()
        else:
            flash("Unable to find record to decline")

    @property
    def isLandlord(self):
        landlordCount = session.query(
            Landlord).filter_by(user_id=self.id).count()

        return landlordCount == 1

    def leaveGroup(self, group):
        # Me must check that this group doesn't have any group listings
        # that are accepted.

        if group.leader_id == self.id:
            flash(
                "You are the leader of this group, assign a new leader before you can leave", 'warning')
            return False
        else:
            groupListings = session.query(GroupListing) \
                .filter_by(group_id=group.id,
                           show=True,
                           completed=True) \
                .count()

            if groupListings == 0:
                groupUser = session.query(GroupUser) \
                    .filter_by(group_id=group.id,
                               user_id=self.id) \
                    .first()

                groupUser.accepted = False
                groupUser.show = False

                session.commit()
                return True
            else:
                flash(
                    "Unable to leave group, Group is a part of a current listing that is accepted", 'warning')
                return False
