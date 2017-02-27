from datetime import datetime as dt

from nexnest.application import db, session, app

from .base import Base

from sqlalchemy import event


# from nexnest.models import direct_message


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
        ########TODODOOOO#########
        # report_group | report_landlord | report_listing | rent_reminder
        ##########################
        # So this is super hacky, and not good to do....
        # but i can't figure out how to do it otherwise
        from nexnest.models.direct_message import DirectMessage
        from nexnest.models.group_listing_message import GroupListingMessage
        from nexnest.models.friend import Friend
        from nexnest.models.group import Group
        from nexnest.models.group_listing import GroupListing
        from nexnest.models.group_listing_favorite import GroupListingFavorite
        from nexnest.models.group_message import GroupMessage
        from nexnest.models.house import House
        from nexnest.models.message import Message
        from nexnest.models.house_message import HouseMessage
        from nexnest.models.platform_report import PlatformReport
        from nexnest.models.security_deposit import SecurityDeposit
        from nexnest.models.maintenance import Maintenance
        from nexnest.models.maintenance_message import MaintenanceMessage
        from nexnest.models.tour import Tour
        from nexnest.models.tour_message import TourMessage

        message = None
        returnObject = None
        redirectURL = None
        if self.type == 'direct_message':
            returnObject = session.query(DirectMessage) \
                .filter_by(user_id=self.target_model_id) \
                .first()

            if returnObject is not None:
                message = "You have recieved a new Direct Message from %s" % returnObject.user.name
                redirectURL = '/user/directMessages/%d' % returnObject.user.id

                return message, returnObject, redirectURL
            else:
                return None, None, None

        elif self.type == 'platform_report':
            returnObject = session.query(PlatformReport) \
                .filter_by(id=self.target_model_id) \
                .first()

            if returnObject is not None:
                message = "There is a new platform report!"

                ##########################
                ######TODDDDDOOOOOOO######
                ##########################
                redirectURL = '/index'

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
                redirectURL = '/index'

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

                redirectURL = '/group/view/%d' % returnObject.id

                return message, returnObject, redirectURL
            else:
                return None, None, None
        elif self.type == 'group_listing_favorite':
            returnObject = session.query(Group) \
                .filter_by(id=self.target_model_id) \
                .first()

            if returnObject is not None:
                message = "A new listing has been suggested to your Group %s" % returnObject.name

                redirectURL = '/group/view/%d' % returnObject.id

                return message, returnObject, redirectURL
            else:
                return None, None, None

        elif self.type == 'group_listing_message':
            returnObject = session.query(GroupListingMessage) \
                .filter_by(id=self.target_model_id) \
                .first()

            if returnObject is not None:
                message = "You have new messages in %s's House Request" % returnObject.groupListing.group.name

                redirectURL = '/houseRequest/view/%d' % returnObject.groupListing.id
                return message, returnObject, redirectURL
            else:
                return None, None, None

        elif self.type == 'group_message':
            returnObject = session.query(GroupMessage) \
                .filter_by(id=self.target_model_id) \
                .first()

            if returnObject is not None:
                message = "You have a new message in %s" % returnObject.group.name

                redirectURL = '/group/view/%d' % returnObject.id

                return message, returnObject, redirectURL
            else:
                return None, None, None

        # If a house request has been accepted + completed, a house
        # notification gets created.
        elif self.type == 'house':
            returnObject = session.query(House) \
                .filter_by(id=self.target_model_id) \
                .first()

            if returnObject is not None:
                message = "Congratulations! %s has accepted your Housing Request, Click here to go to your new humble abode!" % \
                    returnObject.listing.landLordsAsUsers()[0].name

                redirectURL = '/house/view/%d' % returnObject.id

                return message, returnObject, redirectURL
            else:
                return None, None, None

        elif self.type == 'house_message':
            returnObject = session.query(HouseMessage) \
                .filter_by(id=self.target_model_id) \
                .first()

            if returnObject is not None:
                message = "You have a new message in %s's House" % returnObject.house.group.name

                redirectURL = '/house/view/%d' % returnObject.house.id

                return message, returnObject, redirectURL
            else:
                return None, None, None

        elif self.type == 'group_listing_favorite':
            returnObject = session.query(GroupListingFavorite) \
                .filter_by(id=self.target_model_id) \
                .first()

            if returnObject is not None:
                message = "%s has favorited a new listing in %s" % \
                    (returnObject.user, returnObject.group.name)

                redirectURL = '/group/view/%d' % returnObject.group.id

                return message, returnObject, redirectURL
            else:
                return None, None, None

        elif self.type == 'maintenance':
            returnObject = session.query(Maintenance) \
                .filter_by(id=self.target_model_id) \
                .first()

            if returnObject is not None:
                message = "There is a new maintenance request for your listing"

                redirectURL = '/house/maintenanceRequest/%d/view' % returnObject.id

                return message, returnObject, redirectURL
            else:
                return None, None, None

        elif self.type == 'security_deposit':
            returnObject = session.query(SecurityDeposit) \
                .filter_by(id=self.target_model_id) \
                .first()

            if returnObject is not None:
                message = "%s has paid their security deposit!" % returnObject.user.name

                redirectURL = '/houseRequest/view/%d' % returnObject.groupListing.id

                return message, returnObject, redirectURL
            else:
                return None, None, None

        elif self.type == 'tour':
            returnObject = session.query(Tour) \
                .filter_by(id=self.target_model_id) \
                .first()

            if returnObject is not None:
                message = "A new tour has been requested for your listing"

                redirectURL = '/tour/view/%d' % returnObject.id

                return message, returnObject, redirectURL
            else:
                return None, None, None

        elif self.type == 'maintenance_message':
            returnObject = session.query(MaintenanceMessage) \
                .filter_by(id=self.target_model_id) \
                .first()

            if returnObject is not None:
                message = "%s has posted a new message in %s's Maintenance Request" % \
                    (returnObject.user.name, returnObject.maintenance.house.group.name)

                redirectURL = '/house/maintenanceRequest/%d/view' % returnObject.id

                return message, returnObject, redirectURL
            else:
                return None, None, None

        elif self.type == 'new_tour_time':
            returnObject = session.query(Tour) \
                .filter_by(id=self.target_model_id) \
                .first()

            if returnObject is not None:
                message = "A revised tour time has been requested for a tour. Click to view"

                redirectURL = '/tour/view/%d' % returnObject.id

                return message, returnObject, redirectURL
            else:
                return None, None, None

        elif self.type == 'tour_message':
            returnObject = session.query(TourMessage) \
                .filter_by(id=self.target_model_id) \
                .first()
            print('bruh %r' % returnObject.id)

            if returnObject is not None:
                message = "%s has posted a new message in %s's Tour Request" % \
                    (returnObject.user.name, returnObject.tour.group.name)

                redirectURL = '/tour/view/%d' % returnObject.id

                return message, returnObject, redirectURL
            else:
                return None, None, None


def update_date_modified(mapper, connection, target):
    # 'target' is the inserted object
    target.date_modified = dt.now().isoformat()  # Update Date Modified


event.listen(Notification, 'before_update', update_date_modified)
