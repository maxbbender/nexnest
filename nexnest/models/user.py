from .base import Base

from nexnest.application import db

from datetime import datetime as dt

from nexnest.utils.password import hash_password

# from sqlalchemy.orm import relationship

from flask.ext.security import UserMixin

from .role import Role


class User(Base, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(128), nullable=False)
    salt = db.Column(db.String(128), nullable=False)
    name = db.Column(db.String(128))
    bio = db.Column(db.Text)
    website = db.Column(db.String(128))
    location = db.Column(db.String(128))
    phone = db.Column(db.String(10))
    dob = db.Column(db.DateTime)
    profile_image = db.Column(db.String(128))
    date_created = db.Column(db.String(128), nullable=False)
    date_modified = db.Column(db.String(128), nullable=False)
    active = db.Column(db.Boolean)
    roles = db.relationship(Role,
                            secondary='user_roles',
                            backref=db.backref('user', lazy='dynamic'))
    # added_friends = relationship

    def __init__(self,
                 username,
                 email,
                 password,
                 name,
                 bio=None,
                 website=None,
                 location=None,
                 phone=None,
                 dob=None,
                 profile_image=None,
                 role=None
                 ):

        self.username = username
        self.email = email

        self.set_password(password)

        self.name = name

        if role is not None:
            self.role = role
        else:
            self.role = "user"

        self.bio = bio
        self.website = website
        self.location = location
        self.phone = phone
        self.dob = dob

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
