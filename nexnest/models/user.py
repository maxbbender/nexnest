from datetime import datetime as dt

from flask import flash, render_template, url_for
from flask import current_app as app
from nexnest import db
from nexnest.models.group_listing import GroupListing
from nexnest.models.group_user import GroupUser
from nexnest.models.landlord import Landlord
from nexnest.models.notification import Notification
from nexnest.utils.email import send_email
from nexnest.utils.password import hash_password
from sqlalchemy.orm import relationship

from .base import Base

import random

from pprint import pformat


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
    landlord_info_filled = db.Column(db.Boolean)
    newsletter = db.Column(db.Boolean)

    # Relationships
    recievedDM = relationship('DirectMessage',
                              lazy='dynamic',
                              backref='target_user',
                              foreign_keys='DirectMessage.target_user_id',
                              )
    groups = relationship("GroupUser", back_populates='user')
    groupLeader = relationship("Group", backref='leader')
    landlord = relationship('Landlord', backref='user')
    securityDeposits = relationship("SecurityDeposit", backref='user')
    maintenanceRequests = relationship("Maintenance", backref='user')
    notifications = relationship(
        "Notification", backref='user', lazy="dynamic")
    messages = relationship('Message', backref='user')
    groupListingFavorites = relationship(
        'GroupListingFavorite', backref='user')
    transactions = relationship('Transaction', backref='user')
    notificationPreference = relationship('NotificationPreference',
                                          uselist=False, back_populates='user')
    individualFavorites = relationship('ListingFavorite', backref='user')
    reports = relationship('Report', backref='user')
    rent = relationship('Rent', backref='user')

    def __init__(self,
                 email,
                 password,
                 fname,
                 lname,
                 school=None,
                 role=None,
                 bio=None,
                 website=None,
                 location=None,
                 phone=None,
                 dob=None,
                 profile_image=None,
                 email_confirmed=False,
                 landlord_info_filled=True,
                 newsletter=True
                 ):
        if school is not None:
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
            self.role = 'user'
        else:
            self.role = role

        profileImages = ['green_default.png', 'blue_default.png', 'red_default.png', 'yellow_default.png', 'orange_default.png']
        if profile_image is None:
            self.profile_image = url_for('static', filename='img/' + random.choice(profileImages))
        else:
            self.profile_image = profile_image

        # Default Values
        now = dt.now().isoformat()  # Current Time to Insert into Datamodels
        self.date_created = now
        self.date_modified = now
        self.active = True

        if app.config['TESTING']:
            self.email_confirmed = True
        else:
            self.email_confirmed = email_confirmed

        self.landlord_info_filled = landlord_info_filled
        self.newsletter = newsletter

    def __repr__(self):
        return '<User %r | %s(%d)>' % (self.username, self.name, self.id)

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
        landlordCount = db.session.query(
            Landlord).filter_by(user_id=self.id).count()

        return landlordCount == 1

    @property
    def isGroupLeader(self):
        return len(self.groupLeader) > 0

    @property
    def isAdmin(self):
        return self.role == 'admin'

    @property
    def houseList(self):
        houseList = []
        for groupUser in self.groups:
            if groupUser.accepted:
                houseObject = {}
                group = groupUser.group

                if len(group.house) > 0:
                    house = group.house[0]
                    houseObject['address'] = house.listing.address
                    houseObject['url'] = url_for('houses.view', id=house.id)

                    houseList.append(houseObject)

        return houseList

    def get_id(self):
        try:
            return unicode(self.id)  # python 2
        except NameError:
            return str(self.id)  # python 3

    def accept_group_invite(self, group):
        group_user = db.session.query(GroupUser).filter_by(
            accepted=False,
            group_id=group.id,
            user_id=self.id).first()

        if group_user is not None:
            group_user.accepted = True
            group_user.genCompletedNotifications()
            db.session.commit()
            flash("Group invite accepted", 'info')
        else:
            flash("Unable to find record to accept")

    def decline_group_invite(self, group):
        group_user = db.session.query(GroupUser).filter_by(
            accepted=False,
            group_id=group.id,
            user_id=self.id).first()

        if group_user is not None:
            group_user.show = False
            db.session.commit()
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
            groupListings = db.session.query(GroupListing) \
                .filter_by(group_id=group.id,
                           group_show=True,
                           completed=True) \
                .count()

            if groupListings == 0:
                groupUser = db.session.query(GroupUser) \
                    .filter_by(group_id=group.id,
                               user_id=self.id) \
                    .first()

                groupUser.accepted = False
                groupUser.show = False

                db.session.commit()

                for user in groupUser.group.acceptedUsers:
                    newNotif = Notification(notif_type='user_leave_group',
                                            target_model_id=groupUser.id,
                                            target_user=user)
                    db.session.add(newNotif)
                    db.session.commit()

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
        app.logger.debug('getMessageNotifications')
        returnList = self.notifications \
            .filter(Notification.category.in_(('direct_message', 'generic_message'))) \
            .distinct(Notification.notif_type, Notification.redirect_url, Notification.viewed) \
            .paginate(1, 10, False).items
        app.logger.debug(pformat(returnList))
        return returnList

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

    # Icon , Message , Title
    def sendEmail(self, emailType, message):
        current_app.logger.debug('User.sendEmail()')
        current_app.logger.debug('EmailType %s' % emailType)
        icon, title, subject = None, None, None

        if emailType == 'tourRequest':
            icon = 'calendar'
            title = 'tour request'
            subject = 'Tour Request'

        elif emailType == 'tourConfirmed':
            icon = 'calendar'
            title = 'tour request approved'
            subject = 'Tour Request Approved'

        elif emailType == 'tourDenied':
            icon = 'calendar'
            title = 'tour request update'
            subject = 'Tour Request Update'

        elif emailType == 'tourTimeChange':
            icon = 'calendar'
            title = 'new tour time request'
            subject = 'Tour Request Update'

        elif emailType == 'maintenanceCreate':
            icon = 'wrench'
            title = 'maintenance request'
            subject = 'Maintenance Request'

        elif emailType == 'maintenanceInProgress':
            icon = 'wrench'
            title = 'maintenance request'
            subject = 'Maintenance Request Update'

        elif emailType == 'maintenanceCompleted':
            icon = 'wrench'
            title = 'maintenance request'
            subject = 'Maintenance Request Update'

        elif emailType == 'maintenanceMessage':
            icon = 'comments'
            title = 'new message | maintenance'
            subject = 'New Message - Maintenance Request'

        elif emailType == 'groupListingCreate':
            icon = 'home'
            title = 'house request'
            subject = 'House Request'

        elif emailType == 'groupListingDenied':
            icon = 'times-circle'
            title = 'housing request denied'
            subject = 'House Request Update'

        elif emailType == 'groupListingAccepted':
            icon = 'check'
            title = 'housing request approved'
            subject = 'House Request Update'

        elif emailType == 'groupUserCompleted':
            icon = 'user'
            title = 'new group user'
            subject = 'Group Update'

        elif emailType == 'groupListingFavorite':
            icon = 'thumbs-up'
            title = 'Listing Favorite'
            subject = 'Listing Favorite'

        elif emailType == 'houseMessage':
            icon = 'comments'
            title = 'new message | house'
            subject = 'New Message - House'

        elif emailType == 'tourMessage':
            icon = 'comments'
            title = 'new message | tour'
            subject = 'New Message - Tour'

        elif emailType == 'directMessage':
            icon = 'comments'
            title = 'new message | direct'
            subject = 'New Message - Direct'

        elif emailType == 'groupMessage':
            icon = 'comments'
            title = 'new message | group'
            subject = 'New Message - Group'

        elif emailType == 'house':
            icon = 'check'
            title = 'housing request approved'
            subject = 'House Request Update'

        elif emailType == 'emailVerification':
            icon = 'lock'
            title = 'email verification'
            subject = 'Email Verification'

        send_email(subject='NexNest - %s' % subject,
                   sender='no_reply@nexnest.com',
                   recipients=[self.email],
                   html_body=render_template('email/emailTemplate.html',
                                             user=self,
                                             messageContent=message,
                                             icon=icon,
                                             messageType=title))

        # fullMessage = None
        # if emailType == 'message':
        #     send_email(subject='NexNest - New Message',
        #                sender='no_reply@nexnest.com',
        #                recipients=[self.email],
        #                html_body=render_template('email/newGroupMessageEmail.html',
        #                                          user=self,
        #                                          message=message))
        # elif emailType == 'generic':
        #     send_email(subject='NexNest - New Message',
        #                sender='no_reply@nexnest.com',
        #                recipients=[self.email],
        #                html_body=render_template('email/generic.html',
        #                                          user=self,
        #                                          message=message))

    def isEditableBy(self, user, toFlash=False):
        if user.id == self.id:
            return True

        if toFlash:
            flash('Permissions Error', 'danger')

        return False
