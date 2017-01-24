from flask import Blueprint, request, redirect, flash, render_template, url_for

from flask_login import current_user, login_required

from nexnest.application import session

from nexnest.forms import TourForm, TourMessageForm, TourDateChangeForm

from nexnest.models.tour import Tour
from nexnest.models.listing import Listing
from nexnest.models.group import Group
from nexnest.models.tour_messages import TourMessage

from flask.utils.flash import flash_errors

from sqlalchemy import asc

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

            if group is not None:  # Group Exists
                if group.leader == current_user:
                    # At this point we have a valid group and listing
                    # to create the tour request
                    newTour = Tour(listing=listing,
                                   group=group,
                                   time_requested=tourForm.time_requested.data)

                    session.add(newTour)
                    session.commit()

                    # Create the first tour message
                    newTourMessage = TourMessage(tour=newTour,
                                                 content=tourForm.description.data,
                                                 user=current_user)

                    session.add(newTourMessage)
                    session.commit()

                    flash('Tour Request Created', 'info')
                    return redirect(url_for('tours.viewTour', tourID=newTour.id))
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


# What mike needs
# tour, landlords=[Landlords(As users)], messages, tourMessageForm, changeTourDateForm,
@tours.route('/tour/view/<tourID>')
@login_required
def viewTour(tourID):
    tour = session.query(Tour).filter_by(id=tourID).first()

    messageForm = TourMessageForm()
    dateChangeForm = TourDateChangeForm()

    isLandlord = False

    # First lets check the current user is the landlord of
    # the listing that this tour is for
    for landlord in tour.listing.landlord:
        if current_user == landlord.user:
            isLandlord = True

    if tour.group in current_user.accepted_groups or isLandlord:

        # landlords=[Landlords(As users)]
        landlordListingArray = tour.listing.landlords

        landlords = []

        for landlordListing in landlordListingArray:
            landlords.append(landlordListing.landlord.user)

        # Tour Messages
        messages = session.query(TourMessage) \
            .filter_by(tour_id=tour.id) \
            .order_by(asc(TourMessage.date_created)) \
            .all()

        return render_template('viewTour.html',
                               tour=tour,
                               landlords=landlords,
                               messages=messages,
                               messageForm=messageForm,
                               dateChangeForm=dateChangeForm
                               )
    else:
        flash("You are not a part of this tour", 'info')
        return redirect(request.url)
