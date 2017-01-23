from flask import Blueprint, request, redirect, flash

from flask_login import current_user, login_required

from nexnest.application import session

from nexnest.forms.tourForm import TourForm

from nexnest.models.tour import Tour
from nexnest.models.listing import Listing
from nexnest.models.group import Group
from nexnest.models.tour_messages import TourMessage

from flask.utils.flash import flash_errors

tours = Blueprint('tours', __name__, template_folder='../templates/tour')


@tours.route('/tour/create', methods=['POST'])
@login_required
def createTour():
    tourForm = TourForm(request.form)

    if tourForm.validate():
        # Lets find the listing
        listing = session.query(Listing) \
        .filter_by(id=tourForm.listing_id.data) \
        .first()

        if listing is not None:  # Listing exists

            # Lets find the group
            group = session.query(Group) \
            .filter_by(id=tourForm.group_id.data) \
            .first()

            if group is not None: # Group Exists
            	if group.leader == current_user:
            		# At this point we have a valid group and listing
	                # to create the tour request
	                newTour = Tour(listing=listing,
	                               group=group,
	                               time_requested=tourForm.time_requested.data)

	                session.add(newTour)
	                session.commit()
	            else:
	            	flash("Unable to request a tour if you are not the group leader", 'warning')
	            	redirect(request.url)

                
            else:
                flash("Group does not exist", 'warning')
                return redirect(request.url)

        else:
            flash("Listing does not exist", 'warning')
            return redirect(request.url)

    else:
        flash_errors(tourForm)
        return redirect(request.url)
