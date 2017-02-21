from datetime import datetime as dt

from nexnest.application import db, session, app

from .base import Base

from sqlalchemy import event

from nexnest.models import *

from flask import url_for


class Notification(Base):
    __tablename__ = 'notifications'
    id = db.Column(db.Integer, primary_key=True)
    target_user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    target_model_id = db.Column(db.Integer)
    viewed = db.Column(db.Boolean)
    date_created = db.Column(db.DateTime)
    date_modified = db.Column(db.DateTime)

    # Notification Type: Can be the following values
    # | direct_message        | friend        | group_user       | group_listing
    # | group_listing_message | group_message | house            | house_message
    # | group_listing_favorite| maintenance   | platform_report  | report_group
    # | report_landlord       | report_listing| security_deposit | tour
    # | maintenance_message   | rent_reminder | new_tour_time    | tour_message 
    type = db.Column(db.String(128))

    def __init__(
            self,
            target_user,
            target_model_id,
            type
    ):
        self.target_user_id = target_user.id
        self.target_model_id = target_model_id
        self.type = type
        self.viewed = False

        # Default Values
        now = dt.now().isoformat()  # Current Time to Insert into Datamodels
        self.date_created = now
        self.date_modified = now

    def __repr__(self):
        return '<Notification %r>' % self.id


    @property
    def message(self):
        message, returnObject, redirectURL = self.getNotification()
        return message

    @property
    def returnObject(self):
        message, returnObject, redirectURL = self.getNotification()
        return returnObject

    @property
    def redirectURL(self):
        message, returnObject, redirectURL = self.getNotification()
        return redirectURL


    def getNotification(self):
        message = None
        returnObject = None
        redirectURL = None
        if self.type == 'direct_message':
            returnObject = session.query(DirectMessage) \
                .filter_by(target_user_id=self.target_model_id) \
                .first()

            if returnObject is not None:
                message = "You have recieved a new Direct Message from %s" %  \
                    returnObject.source_user.fname
                redirectURL = url_for('users.directMessagesIndividual', user_id=returnObject.target_user_id)

                return message, returnObject, redirectURL
            else:
                return None, None, None
        elif self.type == 'friend':
            returnObject = session.query(Friend) \
                .filter_by(target_user_id=self.target_model_id) \
                .first()

            if returnObject is not None:
                message = "You have recieved a new Friend Request from %s" %  \
                    returnObject.source_user.fname

                ##########################
                ######TODDDDDOOOOOOO######
                ##########################
                redirectURL = url_for('indexs.index')

                return message, returnObject, redirectURL
            else:
                return None, None, None
        elif self.type == 'group_user':
            returnObject = session.query(Group) \
                .filter_by(id=self.target_model_id) \
                .first()

            if returnObject is not None:
                message = "You have recieved a Group Invitation for %s from %s" %  \
                    (returnObject.name, returnObject.leader.fname)

                redirectURL = url_for('groups.view', group_id=returnObject.id)

                return message, returnObject, redirectURL
            else:
                return None, None, None
        elif self.type == 'group_listing_favorite':
            returnObject = session.query(Group) \
                .filter_by(id=self.target_model_id) \
                .first()

            if returnObject is not None:
                message = "A new listing has been suggested to your Group %s" % returnObject.name

                redirectURL = url_for('groups.view', group_id=returnObject.id)

                return message, returnObject, redirectURL
            else:
                return None, None, None

        elif self.type == 'group_listing_message':
            returnObject = session.query(GroupListing) \
                .filter_by(id=self.target_model_id) \
                .first()

            if returnObject is not None:
                message = "You have new messages in %s's House Request" % returnObject.group.name

                redirectURL = url_for('housingRequests.view', id=returnObject.id)

                return message, returnObject, redirectURL
            else:
                return None, None, None



def update_date_modified(mapper, connection, target):
    # 'target' is the inserted object
    target.date_modified = dt.now().isoformat()  # Update Date Modified


event.listen(Notification, 'before_update', update_date_modified)
