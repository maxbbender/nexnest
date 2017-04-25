from datetime import datetime as dt

from sqlalchemy.orm import relationship

from flask import flash, render_template

from nexnest import logger
from nexnest.application import db, session
from nexnest.utils.password import hash_password
from nexnest.utils.email import send_email
from nexnest.models.group_user import GroupUser
from nexnest.models.group_listing import GroupListing
from nexnest.models.notification import Notification
from nexnest.models.landlord import Landlord

from .base import Base


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
    date_created = db.Column(db.DateTime, nullable=False)
    date_modified = db.Column(db.DateTime, nullable=False)
    school_id = db.Column(db.Integer(), db.ForeignKey('schools.id'))
    active = db.Column(db.Boolean)
    email_confirmed = db.Column(db.Boolean)
    # twitter_token = db.Column(db.Text)
    # twitter_secret = db.Column(db.Text)
    # sentDM = relationship('DirectMessage',  # direct_message.DirectMessage
    #                       lazy='dynamic',
    #                       backref='source_user',
    #                       foreign_keys=direct_message.DirectMessage.source_user_id
    #                       # foreign_keys='[DirectMessage.source_user_id]',
    #                       )
    # sentMessages = relationship('Message', backref='user')
    recievedDM = relationship('DirectMessage',
                              lazy='dynamic',
                              backref='target_user',
                              # foreign_keys=direct_message.DirectMessage.target_user_id
                              foreign_keys='DirectMessage.target_user_id',
                              )
    groups = relationship("GroupUser", back_populates='user')
    groupLeader = relationship("Group", backref='leader')
    # groupMessages = relationship("GroupMessage", backref='user')
    # houseMessages = relationship("HouseMessage", backref='user')
    landlord = relationship('Landlord', backref='user')
    # tourMessages = relationship("TourMessage", backref='user')
    # groupListingMessages = relationship("GroupListingMessage", backref='user')
    securityDeposits = relationship("SecurityDeposit", backref='user')
    # maintenanceMessages = relationship("MaintenanceMessage", backref='user')
    maintenanceRequests = relationship("Maintenance", backref='user')
    notifications = relationship("Notification", backref='user', lazy="dynamic")
    messages = relationship('Message', backref='user')
    groupListingFavorites = relationship('GroupListingFavorite', backref='user')
    transactions = relationship('Transaction', backref='user')
    notificationPreference = relationship('NotificationPreference', uselist=False, back_populates='user')

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
                 email_confirmed=False
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

        if profile_image is None:
            self.profile_image = "https://api.adorable.io/avatars/120/" + self.username
        else:
            self.profile_image = profile_image

        # Default Values
        now = dt.now().isoformat()  # Current Time to Insert into Datamodels
        self.date_created = now
        self.date_modified = now
        self.active = True
        self.email_confirmed = email_confirmed

    def __repr__(self):
        return '<User %r | %s>' % (self.username, self.name)

    @property
    def serialize(self):
        return {
            'id': self.id,
            'username': self.username,
            'fname': self.fname,
            'lname': self.lname,
            'profileImageURL': self.profile_image,
            'url': '/user/view/%d' % self.id
        }

    @property
    def shortSerialize(self):
        return {
            'name': self.name,
            'id': self.id,
            'profileImageURL': self.profile_image,
            'url': '/user/view/%d' % self.id
        }

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

    @property
    def name(self):
        return "%s %s" % (self.fname, self.lname)

    @property
    def isLandlord(self):
        landlordCount = session.query(
            Landlord).filter_by(user_id=self.id).count()

        return landlordCount == 1

    @property
    def isGroupLeader(self):
        return len(self.groupLeader) > 0

    @property
    def isAdmin(self):
        return self.role == 'admin'

    def get_id(self):
        try:
            return unicode(self.id)  # python 2
        except NameError:
            return str(self.id)  # python 3

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
                           group_show=True,
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

                for user in groupUser.group.acceptedUsers:
                    newNotif = Notification(notif_type='user_leave_group',
                                            target_model_id=groupUser.id,
                                            target_user=user)
                    session.add(newNotif)
                    session.commit()

                return True
            else:
                flash(
                    "Unable to leave group, Group is a part of a current listing that is accepted", 'warning')
                return False

    def getNotifications(self):
        return self.notifications \
            .filter(Notification.category.in_(('report_notification', 'generic_notification'))) \
            .distinct(Notification.notif_type, Notification.redirect_url, Notification.viewed) \
            .paginate(1, 10, False).items

    def getMessageNotifications(self):
        return self.notifications \
            .filter(Notification.category.in_(('direct_message', 'generic_message'))) \
            .distinct(Notification.notif_type, Notification.redirect_url, Notification.viewed) \
            .paginate(1, 10, False).items

    def getUnreadMessageNotificationCount(self):
        return self.notifications \
            .filter(Notification.viewed == False) \
            .filter(Notification.category.in_(('direct_message', 'generic_message'))) \
            .distinct(Notification.notif_type, Notification.redirect_url, Notification.viewed) \
            .count()

    def getUnreadNotificationCount(self):
        return self.notifications \
            .filter(Notification.viewed == False) \
            .filter(Notification.category.in_(('report_notification', 'generic_notification'))) \
            .distinct(Notification.notif_type, Notification.redirect_url, Notification.viewed) \
            .count()

    def sendEmail(self, emailType, message):
        logger.debug('User.sendEmail()')
        logger.debug('EmailType %s' % emailType)
        # fullMessage = None
        if emailType == 'message':
            send_email(subject='NexNest - New Message',
                       sender='no_reply@nexnest.com',
                       recipients=[self.email],
                       html_body=render_template('email/newMessage.html',
                                                 user=self,
                                                 message=message))
        elif emailType == 'generic':
            send_email(subject='NexNest - New Message',
                       sender='no_reply@nexnest.com',
                       recipients=[self.email],
                       html_body=render_template('email/generic.html',
                                                 user=self,
                                                 message=message))
