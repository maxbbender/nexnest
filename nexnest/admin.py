from nexnest import app
from nexnest.models import *
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView


class AdminModelView(ModelView):
    def is_accessible(self):
        return True
        # return current_user.isAdmin # TURN ON FOR PRODUCTION

    def inaccessible_callback(self, name, **kwargs):
        # redirect to login page if user doesn't have access
        return redirect(url_for('indexs.index'))


admin = Admin(app, name='Nexnest', template_mode='bootstrap3')

# Register the Views
admin.add_view(AdminModelView(user.User, session))
admin.add_view(AdminModelView(group.Group, session))
admin.add_view(AdminModelView(listing.Listing, session))
admin.add_view(AdminModelView(message.Message, session))
admin.add_view(AdminModelView(landlord.Landlord, session))
admin.add_view(AdminModelView(school.School, session))
admin.add_view(AdminModelView(tour.Tour, session))
admin.add_view(AdminModelView(tour_message.TourMessage, session))
admin.add_view(AdminModelView(group_message.GroupMessage, session))
admin.add_view(AdminModelView(direct_message.DirectMessage, session))
admin.add_view(AdminModelView(group_listing.GroupListing, session))
admin.add_view(AdminModelView(notification.Notification, session))
admin.add_view(AdminModelView(group_listing_favorite.GroupListingFavorite, session))
