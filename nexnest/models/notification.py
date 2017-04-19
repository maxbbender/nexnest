from datetime import datetime as dt

from sqlalchemy import event
from flask import flash

from nexnest.application import db, session
from nexnest.models.base import Base


class Notification(Base):
    __tablename__ = 'notifications'
    id = db.Column(db.Integer, primary_key=True)
    target_user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    target_model_id = db.Column(db.Integer)
    viewed = db.Column(db.Boolean)
    category = db.Column(db.Text)
    date_created = db.Column(db.DateTime)
    date_modified = db.Column(db.DateTime)

    # Notification Type: Can be the following values
    # | direct_message        | friend        | group_user       | group_listing
    # | group_listing_message | group_message | house            | house_message
    # | group_listing_favorite| maintenance   | platform_report  | report_group
    # | report_landlord       | report_listing| security_deposit | tour
    # | maintenance_message   | rent_reminder | new_tour_time    | tour_message
    # ----------------------------------------------------------------b#
    # NEW ONES (need category):
    # | user_leave_group | maintenance_inprogress | maintenance_completed
    # | group_listing_accept | group_listing_denied | tour_confirm | tour_denied
    notif_type = db.Column(db.String(128))
    redirect_url = db.Column(db.String(128))
    message = db.Column(db.Text)

    def __init__(
            self,
            target_user,
            target_model_id,
            notif_type
    ):
        self.target_user_id = target_user.id
        self.target_model_id = target_model_id
        self.notif_type = notif_type
        self.viewed = False

        # Default Values
        now = dt.now().isoformat()  # Current Time to Insert into Datamodels
        self.date_created = now
        self.date_modified = now

        generic_message = ['group_listing_message', 'group_message',
                           'house_message', 'tour_message',
                           'maintenance_message']

        report_notification = ['platform_report', 'report_group',
                               'report_landlord', 'report_listing']

        if self.notif_type == 'direct_message':
            self.category = 'direct_message'
        elif self.notif_type in generic_message:
            self.category = 'generic_message'
        elif self.notif_type in report_notification:
            self.category = 'report_notification'
        else:
            self.category = 'generic_notification'

        message, returnObject, redirectURL = self.getNotification()  # pylint: disable=unused-variable
        self.message = message
        self.redirect_url = redirectURL

    def __repr__(self):
        return '<Notification %r>' % self.id

    @property
    def serialize(self):
        return {
            'target_user': self.user.serialize,
            'viewed': self.viewed,
            'notif_type': self.notif_type,
            'message': self.message,
            'redirectURL': self.redirect_url,
            'category': self.category
        }

    @property
    def returnObject(self):
        message, returnObject, redirectURL = self.getNotification()  # pylint: disable=unused-variable
        return returnObject

    @property
    def redirectURL(self):
        return self.redirect_url

    def isViewableBy(self):
        return True

    def isEditableBy(self, user, toFlash=False):
        if self.user == user:
            return True
        else:
            if toFlash:
                flash('Permissions Error', 'warning')
                return False

    def getNotification(self):
        # #######TODODOOOO######## #
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
        from nexnest.models.house_message import HouseMessage
        from nexnest.models.platform_report import PlatformReport
        from nexnest.models.security_deposit import SecurityDeposit
        from nexnest.models.maintenance import Maintenance
        from nexnest.models.maintenance_message import MaintenanceMessage
        from nexnest.models.tour import Tour
        from nexnest.models.tour_message import TourMessage
        from nexnest.models.group_user import GroupUser

        message = None
        returnObject = None
        redirectURL = None
        if self.notif_type == 'direct_message':
            returnObject = session.query(DirectMessage) \
                .filter_by(user_id=self.target_model_id) \
                .first()

            if returnObject is not None:
                message = "Direct Message from %s" % returnObject.user.name
                redirectURL = '/user/directMessages/%d' % returnObject.user.id

                return message, returnObject, redirectURL

        elif self.notif_type == 'platform_report':
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

        elif self.notif_type == 'friend':
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
        elif self.notif_type == 'group_user':
            returnObject = session.query(Group) \
                .filter_by(id=self.target_model_id) \
                .first()

            if returnObject is not None:
                message = "You have recieved a Group Invitation for %s from %s" %  \
                    (returnObject.name, returnObject.leader.fname)

                redirectURL = '/group/view/%d' % returnObject.id

                return message, returnObject, redirectURL
        elif self.notif_type == 'group_listing_message':
            returnObject = session.query(GroupListingMessage) \
                .filter_by(id=self.target_model_id) \
                .first()

            if returnObject is not None:
                message = "New messages in %s's House Request" % returnObject.groupListing.group.name

                redirectURL = '/houseRequest/view/%d' % returnObject.groupListing.id
                return message, returnObject, redirectURL

        elif self.notif_type == 'group_message':
            returnObject = session.query(GroupMessage) \
                .filter_by(id=self.target_model_id) \
                .first()

            if returnObject is not None:
                message = "New message in %s" % returnObject.group.name

                redirectURL = '/group/view/%d' % returnObject.id

                return message, returnObject, redirectURL

        # If a house request has been accepted + completed, a house
        # notification gets created.
        elif self.notif_type == 'house':
            returnObject = session.query(House) \
                .filter_by(id=self.target_model_id) \
                .first()

            if returnObject is not None:
                message = "Congratulations! %s has accepted your Housing Request, Click here to go to your new humble abode!" % \
                    returnObject.listing.landLordsAsUsers()[0].name

                redirectURL = '/house/view/%d' % returnObject.id

                return message, returnObject, redirectURL

        elif self.notif_type == 'house_message':
            returnObject = session.query(HouseMessage) \
                .filter_by(id=self.target_model_id) \
                .first()

            if returnObject is not None:
                message = "New message in %s's House" % returnObject.house.group.name

                redirectURL = '/house/view/%d' % returnObject.house.id

                return message, returnObject, redirectURL

        elif self.notif_type == 'group_listing_favorite':
            returnObject = session.query(GroupListingFavorite) \
                .filter_by(id=self.target_model_id) \
                .first()

            if returnObject is not None:
                message = "%s has favorited a new listing in %s" % \
                    (returnObject.user.name, returnObject.group.name)

                redirectURL = '/group/view/%d' % returnObject.group.id

                return message, returnObject, redirectURL

        elif self.notif_type == 'maintenance':
            returnObject = session.query(Maintenance) \
                .filter_by(id=self.target_model_id) \
                .first()

            if returnObject is not None:
                message = "There is a new maintenance request for your listing"

                redirectURL = '/house/maintenanceRequest/%d/view' % returnObject.id

                return message, returnObject, redirectURL

        elif self.notif_type == 'security_deposit':
            returnObject = session.query(SecurityDeposit) \
                .filter_by(id=self.target_model_id) \
                .first()

            if returnObject is not None:
                message = "%s has paid their security deposit!" % returnObject.user.name

                redirectURL = '/houseRequest/view/%d' % returnObject.groupListing.id

                return message, returnObject, redirectURL

        elif self.notif_type == 'tour':
            returnObject = session.query(Tour) \
                .filter_by(id=self.target_model_id) \
                .first()

            if returnObject is not None:
                message = "A new tour has been requested for your listing"

                redirectURL = '/tour/view/%d' % returnObject.id

                return message, returnObject, redirectURL

        elif self.notif_type == 'maintenance_message':
            returnObject = session.query(MaintenanceMessage) \
                .filter_by(id=self.target_model_id) \
                .first()

            if returnObject is not None:
                message = "%s has posted a new message in %s's Maintenance Request" % \
                    (returnObject.user.name, returnObject.maintenance.house.group.name)

                redirectURL = '/house/maintenanceRequest/%d/view' % returnObject.maintenance.id

                return message, returnObject, redirectURL

        elif self.notif_type == 'new_tour_time':
            returnObject = session.query(Tour) \
                .filter_by(id=self.target_model_id) \
                .first()

            if returnObject is not None:
                message = "A revised tour time has been requested for a tour."

                redirectURL = '/tour/view/%d' % returnObject.id

                return message, returnObject, redirectURL

        elif self.notif_type == 'tour_message':
            returnObject = session.query(TourMessage) \
                .filter_by(id=self.target_model_id) \
                .first()

            if returnObject is not None:
                message = "%s has posted a new message in %s's Tour Request" % \
                    (returnObject.user.name, returnObject.tour.group.name)

                redirectURL = '/tour/view/%d' % returnObject.id

                return message, returnObject, redirectURL
        elif self.notif_type == 'group_listing':
            returnObject = session.query(GroupListing) \
                .filter_by(id=self.target_model_id) \
                .first()

            if returnObject is not None:
                message = "You have a new House Request from %s" % \
                    (returnObject.group.name)

                redirectURL = '/houseRequest/view/%d' % returnObject.id

                return message, returnObject, redirectURL

        elif self.notif_type == 'user_leave_group':
            returnObject = session.query(GroupUser) \
                .filter_by(id=self.target_model_id) \
                .first()

            if returnObject is not None:
                message = "%s has left %s" % \
                    (returnObject.user.name, returnObject.group.name)

                redirectURL = '/group/view/%d' % returnObject.group.id

                return message, returnObject, redirectURL

        elif self.notif_type == 'maintenance_inprogress':
            returnObject = session.query(Maintenance) \
                .filter_by(id=self.target_model_id) \
                .first()

            if returnObject is not None:
                message = "Your landlord has marked your maintenance request as In Progress!"

                redirectURL = '/house/maintenanceRequest/%d/view' % returnObject.id

                return message, returnObject, redirectURL

        elif self.notif_type == 'maintenance_completed':
            returnObject = session.query(Maintenance) \
                .filter_by(id=self.target_model_id) \
                .first()

            if returnObject is not None:
                message = "Your landlord has marked your maintenance request as Completed!"

                redirectURL = '/house/maintenanceRequest/%d/view' % returnObject.id

                return message, returnObject, redirectURL

        elif self.notif_type == 'group_listing_accept':
            returnObject = session.query(GroupListing) \
                .filter_by(id=self.target_model_id) \
                .first()

            if returnObject is not None:
                message = "Your house request has been accepted!"

                redirectURL = '/houseRequest/view/%d' % returnObject.id

                return message, returnObject, redirectURL

        elif self.notif_type == 'group_listing_denied':
            returnObject = session.query(GroupListing) \
                .filter_by(id=self.target_model_id) \
                .first()

            if returnObject is not None:
                message = "Your house request for %s has been denied" % returnObject.listing.street

                redirectURL = '/'

                return message, returnObject, redirectURL

        elif self.notif_type == 'group_listing_completed':
            returnObject = session.query(GroupListing) \
                .filter_by(id=self.target_model_id) \
                .first()

            if returnObject is not None:
                message = "Your house request for %s has been completed : Click to go to your new House!" % returnObject.listing.street

                newHouse = session.query(House) \
                    .filter_by(group_id=returnObject.group.id) \
                    .first()

                if newHouse is not None:
                    redirectURL = '/house/view/%d' % newHouse.id
                else:
                    redirectURL = '/'

                return message, returnObject, redirectURL

        elif self.notif_type == 'tour_confirmed':
            returnObject = session.query(Tour) \
                .filter_by(id=self.target_model_id) \
                .first()

            if returnObject is not None:
                message = 'Your tour has been confirmed!'

                redirectURL = '/tour/view/%d' % returnObject.id

                return message, returnObject, redirectURL

        elif self.notif_type == 'tour_denied':
            returnObject = session.query(Tour) \
                .filter_by(id=self.target_model_id) \
                .first()

            if returnObject is not None:
                message = 'Your request for a tour at %s has been denied' % returnObject.listing.street

                redirectURL = '/group/view/%d' % returnObject.group.id

                return message, returnObject, redirectURL

        return None, None, None


def update_date_modified(mapper, connection, target):  # pylint: disable=unused-argument
    # 'target' is the inserted object
    target.date_modified = dt.now().isoformat()  # Update Date Modified


event.listen(Notification, 'before_update', update_date_modified)
