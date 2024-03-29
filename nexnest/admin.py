from flask import current_app as app

from nexnest import db, admin
from nexnest.models.notification_preference import NotificationPreference
from nexnest.models.user import User
from nexnest.models.report import Report
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
from nexnest.models.report_landlord import ReportLandlord
from nexnest.models.report_listing import ReportListing
from nexnest.models.report_group import ReportGroup
from nexnest.models.platform_report import PlatformReport
from nexnest.models.availability import Availability
from nexnest.models.tour_time import TourTime
from nexnest.models.group_email import GroupEmail
from nexnest.models.rent import Rent


from flask import redirect, url_for
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user

session = db.session


class AdminModelView(ModelView):
    column_display_pk = True

    def is_accessible(self):
        if app.config['TESTING'] or app.config['DEBUG']:
            return True
        else:
            if current_user.is_authenticated:
                return current_user.isAdmin
            else:
                return False

    def inaccessible_callback(self, name, **kwargs):
        # redirect to login page if user doesn't have access
        return redirect(url_for('indexs.index'))


# Register the Views
# ----------------------
# -------USERS---------
# ----------------------
admin.add_view(AdminModelView(User, session))
admin.add_view(AdminModelView(Landlord, session))
admin.add_view(AdminModelView(School, session))
admin.add_view(AdminModelView(NotificationPreference, session))
admin.add_view(AdminModelView(Availability, session))
admin.add_view(AdminModelView(TourTime, session))

# ----------------------
# -------GROUPS---------
# ----------------------
admin.add_view(AdminModelView(Group, session))
admin.add_view(AdminModelView(GroupUser, session))
admin.add_view(AdminModelView(GroupListingFavorite, session))
admin.add_view(AdminModelView(GroupEmail, session))
admin.add_view(AdminModelView(GroupListing, session))
admin.add_view(AdminModelView(Tour, session))

# ----------------------
# ------LISTINGS--------
# ----------------------
admin.add_view(AdminModelView(Listing, session))
admin.add_view(AdminModelView(ListingTransaction, session))
admin.add_view(AdminModelView(ListingTransactionListing, session))
admin.add_view(AdminModelView(ListingSchool, session))
admin.add_view(AdminModelView(ListingFavorite, session))
admin.add_view(AdminModelView(LandlordListing, session))

# ----------------------
# ------MESSAGES--------
# ----------------------
admin.add_view(AdminModelView(Message, session))
admin.add_view(AdminModelView(TourMessage, session))
admin.add_view(AdminModelView(GroupMessage, session))
admin.add_view(AdminModelView(DirectMessage, session))
admin.add_view(AdminModelView(GroupListingMessage, session))

# ---------------------
# ------REPORTS--------
# ---------------------
admin.add_view(AdminModelView(Report, session))
admin.add_view(AdminModelView(ReportLandlord, session))
admin.add_view(AdminModelView(ReportGroup, session))
admin.add_view(AdminModelView(ReportListing, session))
admin.add_view(AdminModelView(PlatformReport, session))

# -------------------
# ------HOUSE--------
# -------------------
admin.add_view(AdminModelView(House, session))
admin.add_view(AdminModelView(Rent, session))
admin.add_view(AdminModelView(Maintenance, session))

# ------------------
# ------MISC--------
# ------------------
admin.add_view(AdminModelView(Notification, session))
admin.add_view(AdminModelView(SecurityDeposit, session))
admin.add_view(AdminModelView(Coupon, session))
