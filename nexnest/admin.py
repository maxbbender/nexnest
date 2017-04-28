from nexnest import app
from nexnest.application import session
from nexnest.models.notification_preference import NotificationPreference
from nexnest.models.user import User
from nexnest.models.group import Group
from nexnest.models.listing import Listing
from nexnest.models.message import Message
from nexnest.models.landlord import Landlord
from nexnest.models.landlord_listing import LandlordListing
from nexnest.models.school import School
from nexnest.models.listing_school import ListingSchool
from nexnest.models.tour import Tour
from nexnest.models.tour_message import TourMessage
from nexnest.models.group_message import GroupMessage
from nexnest.models.direct_message import DirectMessage
from nexnest.models.group_listing import GroupListing
from nexnest.models.notification import Notification
from nexnest.models.group_listing_favorite import GroupListingFavorite
from nexnest.models.security_deposit import SecurityDeposit
from nexnest.models.house import House
from nexnest.models.maintenance import Maintenance
from nexnest.models.group_listing_message import GroupListingMessage
from nexnest.models.group_user import GroupUser
from nexnest.models.coupon import Coupon
from nexnest.models.listing_favorite import ListingFavorite
from nexnest.models.transaction import *

from flask import redirect, url_for
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView


class AdminModelView(ModelView):
    column_display_pk = True

    def is_accessible(self):
        return True
        # return current_user.isAdmin # TURN ON FOR PRODUCTION

    def inaccessible_callback(self, name, **kwargs):
        # redirect to login page if user doesn't have access
        return redirect(url_for('indexs.index'))


admin = Admin(app, name='Nexnest', template_mode='bootstrap3')

# Register the Views
admin.add_view(AdminModelView(User, session))
admin.add_view(AdminModelView(Group, session))
admin.add_view(AdminModelView(Listing, session))
admin.add_view(AdminModelView(Message, session))
admin.add_view(AdminModelView(Landlord, session))
admin.add_view(AdminModelView(School, session))
admin.add_view(AdminModelView(Tour, session))
admin.add_view(AdminModelView(TourMessage, session))
admin.add_view(AdminModelView(GroupMessage, session))
admin.add_view(AdminModelView(DirectMessage, session))
admin.add_view(AdminModelView(GroupListing, session))
admin.add_view(AdminModelView(Notification, session))
admin.add_view(AdminModelView(GroupListingFavorite, session))
admin.add_view(AdminModelView(SecurityDeposit, session))
admin.add_view(AdminModelView(House, session))
admin.add_view(AdminModelView(Maintenance, session))
admin.add_view(AdminModelView(GroupListingMessage, session))
admin.add_view(AdminModelView(GroupUser, session))
admin.add_view(AdminModelView(ListingTransaction, session))
admin.add_view(AdminModelView(ListingTransactionListing, session))
admin.add_view(AdminModelView(Coupon, session))
admin.add_view(AdminModelView(ListingSchool, session))
admin.add_view(AdminModelView(LandlordListing, session))
admin.add_view(AdminModelView(NotificationPreference, session))
admin.add_view(AdminModelView(ListingFavorite, session))

