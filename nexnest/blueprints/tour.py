from flask import Blueprint, request, redirect, flash, render_template, url_for, jsonify

from flask_login import current_user, login_required

from nexnest import logger
from nexnest.application import session

from nexnest.forms import TourForm, TourMessageForm, TourDateChangeForm

from nexnest.models.tour import Tour
from nexnest.models.listing import Listing
from nexnest.models.group import Group
from nexnest.models.tour_message import TourMessage
from nexnest.models.tour_time import TourTime

from nexnest.utils.flash import flash_errors
from nexnest.decorators import tour_editable

from sqlalchemy import desc

import json

from dateutil import parser

tours = Blueprint('tours', __name__, template_folder='../templates/tour')


# NOTIFICATIONS IMPLEMENTED
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
                .filter_by(id=tourForm.group_tour_id.data) \
                .first()

            if group is not None:  # Group Exists
                if group.leader == current_user:
                    # At this point we have a valid group and listing
                    # to create the tour request
                    newTour = Tour(listing=listing,
                                   group=group)

                    session.add(newTour)
                    session.commit()

                    newTour.genNotifications()

                    # Create the first tour message
                    newTourMessage = TourMessage(tour=newTour,
                                                 content=tourForm.description.data,
                                                 user=current_user)

                    session.add(newTourMessage)
                    session.commit()

                    newTour.genNotifications()

                    # Generate Tour Times
                    tourTimeJSON = json.loads(tourForm.requestedDateTime.data)
                    logger.debug('tourTimeJSON %r' % tourTimeJSON)
                    for time in tourTimeJSON:
                        timeObject = parser.parse(time)
                        newTourTime = TourTime(newTour, timeObject)
                        session.add(newTourTime)
                        session.commit()

                        logger.debug('time: %s | timeObject %r' % (time, timeObject))

                    flash('Tour Request Created', 'info')
                    return redirect(url_for('tours.viewTour', tourID=newTour.id))
                else:
                    flash("Unable to request a tour if you are not the group leader", 'warning')
                    return redirect(url_for('listings.viewListing', listingID=listing.id))

            else:
                flash("Group does not exist", 'warning')
                return redirect(url_for('listings.viewListing', listingID=listing.id))

        else:
            flash("Listing does not exist", 'warning')
            return redirect(url_for('listings.viewListing', listingID=listing.id))

    else:
        flash_errors(tourForm)
        return redirect(url_for('indexs.index'))


@tours.route('/tour/view/<tourID>')
@login_required
def viewTour(tourID):
    tour = Tour.query.filter_by(id=tourID).first_or_404()

    messageForm = TourMessageForm()
    dateChangeForm = TourDateChangeForm()

    if tour.isViewableBy(current_user):

        # Tour Messages
        messages = session.query(TourMessage) \
            .filter_by(tour_id=tour.id) \
            .order_by(desc(TourMessage.date_created)) \
            .all()

        return render_template('tourView.html',
                               tour=tour,
                               landlords=tour.listing.landLordsAsUsers(),
                               messages=messages,
                               messageForm=messageForm,
                               dateChangeForm=dateChangeForm
                               )
    else:
        flash("You are not a part of this tour", 'info')
        return redirect(url_for('indexs.index'))


@tours.route('/tour/<tourID>/confirm')
@tours.route('/tour/<tourID>/confirm/ajax')
@login_required
@tour_editable
def confirmTour(tourID):
    tour = Tour.query.filter_by(id=tourID).first_or_404()

    errorMessage = None

    if tour is not None:
        if tour.isEditableBy(current_user, toFlash=False):
            tour.tour_confirmed = True
            session.commit()

            tour.genConfirmNotifications()

            if request.is_xhr:
                return jsonify(results={'success': True})
            else:
                return redirect(url_for('tours.viewTour', tourID=tourID))
        else:
            errorMessage = 'Permissions Error'
    else:
        errorMessage = 'Invalid Reqeuest'

    if request.is_xhr:
        return jsonify(results={'success': False, 'message': errorMessage})
    else:
        flash(errorMessage, 'danger')
        return redirect(url_for('tours.viewTour', tourID=tourID))


# NOTIFICATIONS IMPLEMENTED
@tours.route('/tour/<tourID>/unConfirm/ajax')
@login_required
def unConfirmTourAJAX(tourID):
    tour = session.query(Tour) \
        .filter_by(id=tourID) \
        .first()

    errorMessage = None

    if tour is not None:
        if tour.isEditableBy(current_user, toFlash=False):
            tour.tour_confirmed = False
            session.commit()

            tour.undoConfirmNotifications()

            return jsonify(results={'success': True})
        else:
            errorMessage = 'Permissions Error'
    else:
        errorMessage = 'Invalid Reqeuest'

    return jsonify(results={'success': False, 'message': errorMessage})


# NOTIFICATIONS IMPLEMENTED
@tours.route('/tour/<tourID>/updateDate', methods=['POST'])
@login_required
def updateTime(tourID):
    tour = session.query(Tour) \
        .filter_by(id=tourID) \
        .first()

    if tour is not None:
        form = TourDateChangeForm(request.form)

        if form.validate():

            if tour.isEditableBy(current_user):
                tour.time_requested = form.requestedDateTime.data

                if tour.last_requested == 'group':
                    tour.last_requested = 'landlord'
                else:
                    tour.last_requested = 'group'

                tour.genTimeChangeNotifications()

                session.commit()
            else:
                flash("Only Group Leader and Landlord can change time", 'warning')
        else:
            flash_errors(form)
    else:
        flash("Tour does not exist", 'warning')
        return redirect(url_for('indexs.index'))

    return redirect(url_for('tours.viewTour', tourID=tourID))


# NOTIFICATIONS IMPLEMENTED
@tours.route('/tour/createMessage', methods=['POST'])
@login_required
def createMessage():
    form = TourMessageForm(request.form)

    if form.validate():
        tour = session.query(Tour).filter_by(id=form.tour_id.data).first()

        if tour is not None:
            if tour.isViewableBy(current_user):
                newTM = TourMessage(tour=tour,
                                    content=form.content.data,
                                    user=current_user)
                session.add(newTM)
                session.commit()

                newTM.genNotifications()

                return redirect(url_for('tours.viewTour', tourID=tour.id))
        else:
            flash("Tour does not exist", 'warning')
    else:
        flash_errors(form)

    return form.redirect()


# NOTIFICATIONS IMPLEMENTED
@tours.route('/tour/<tourID>/decline/ajax')
@login_required
def declineTourAJAX(tourID):
    tour = session.query(Tour) \
        .filter_by(id=tourID) \
        .first()

    errorMessage = None

    if tour is not None:
        if tour.isEditableBy(current_user, toFlash=False):
            tour.declined = True
            session.commit()

            tour.genDeniedNotifications()

            return jsonify(results={'success': True})
        else:
            errorMessage = 'Permissions Error'
    else:
        errorMessage = 'Invalid Reqeuest'

    return jsonify(results={'success': False, 'message': errorMessage})


# NOTIFICATIONS IMPLEMENTED
@tours.route('/tour/<tourID>/unDecline/ajax')
@login_required
def unDeclineTourAJAX(tourID):
    tour = session.query(Tour) \
        .filter_by(id=tourID) \
        .first()

    errorMessage = None

    if tour is not None:
        if tour.isEditableBy(current_user, toFlash=False):
            tour.declined = False
            session.commit()

            tour.undoDeniedNotifications()

            return jsonify(results={'success': True})
        else:
            errorMessage = 'Permissions Error'
    else:
        errorMessage = 'Invalid Reqeuest'

    return jsonify(results={'success': False, 'message': errorMessage})


# @tours.route('/tour/<tourID>/getTourTimes')
# @login_required
# def getTourTimes(tourID):
#     tour = Tour.query.filter_by(id=tourID).first_or_404()

#     if tour.isViewableBy(current_user):
