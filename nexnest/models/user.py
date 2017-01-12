
from nexnest.application import db, session
from nexnest.utils.password import hash_password

from nexnest.models.direct_message import DirectMessage
from nexnest.models.group import Group
from nexnest.models.group_user import GroupUser

from .base import Base


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
    active = db.Column(db.Boolean)
    sent_direct_messages = relationship(DirectMessage,
                                        backref='source_user',
                                        foreign_keys='[DirectMessage.source_user_id]')
    recieved_direct_messages = relationship(DirectMessage,
                                            backref='target_user',
                                            foreign_keys='[DirectMessage.target_user_id]')
    groups = relationship("GroupUser", back_populates='user')

    groupLeader = relationship("Group", backref='leader')

    def __init__(self,
                 email,
                 password,
                 fname,
                 lname,
                 role=None,
                 bio=None,
                 website=None,
                 location=None,
                 phone=None,
                 dob=None,
                 profile_image=None,
                 ):

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
            if not groupUser.accepted:
                unAcceptedGroups.append(groupUser.group)
                
        return unAcceptedGroups

    def accept_group_invite(self, group):
        group_user = session.query(GroupUser.filter_by(
            accepted=False,
            group_id=group.id,
            user_id=self.id)).first()

        if group_user is not None:
            group_user.accepted = True
            session.commit()
        else:
            flash("Unable to find record to accept")
        
