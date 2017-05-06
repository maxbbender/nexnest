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
from nexnest.decorators import tour_editable, tour_viewable

from sqlalchemy import desc

import json

from dateutil import parser

tours = Blueprint('tours', __name__, template_folder='../templates/tour')


@tours.route('/tour/create', methods=['POST'])
@login_required
def createTour():
    tourForm = TourForm(request.form)

    errorMessage = None

    if tourForm.validate():
        # Lets find the listing
        listing = Listing.query.filter_by(id=tourForm.listing_id.data).first_or_404()

        # Lets find the group
        group = Group.query.filter_by(id=tourForm.group_tour_id.data).first_or_404()

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

            flash('Your request to tour %s has been made. The Landlord will get back to you soon.' % newTour.listing.address,
                  'success')
            return redirect(url_for('tours.viewTour', tourID=newTour.id))
        else:
            flash("Only the Group Leader can request a Tour. Please ask your leader to schedule a tour for this listing", 'warning')
            return redirect(url_for('listings.viewListing', listingID=listing.id))
    else:
        if request.is_xhr:
            return jsonify({'success': False, 'message': errorMessage})
        else:
            flash_errors(tourForm)
            return tourForm.redirect()


@tours.route('/tour/view/<tourID>')
@login_required
@tour_viewable
def viewTour(tourID):
    tour = Tour.query.filter_by(id=tourID).first_or_404()

    messageForm = TourMessageForm()
    dateChangeForm = TourDateChangeForm()

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


@tours.route('/tour/<tourID>/confirm')
@tours.route('/tour/<tourID>/confirm/ajax')
@login_required
@tour_editable
def confirmTour(tourID):
    tour = Tour.query.filter_by(id=tourID).first_or_404()

    tour.tour_confirmed = True
    session.commit()

    tour.genConfirmNotifications()

    if request.is_xhr:
        return jsonify(results={'success': True})
    else:
        return redirect(url_for('tours.viewTour', tourID=tourID))


@tours.route('/tour/<tourID>/unConfirm/ajax')
@login_required
@tour_editable
def unConfirmTourAJAX(tourID):
    tour = Tour.query.filter_by(id=tourID).first_or_404()

    tour.tour_confirmed = False
    session.commit()

    tour.undoConfirmNotifications()

    return jsonify(results={'success': True})


@tours.route('/tour/<tourID>/updateDate', methods=['POST'])
@login_required
@tour_editable
def updateTime(tourID):
    tour = Tour.query.filter_by(id=tourID).first_or_404()

    form = TourDateChangeForm(request.form)

    if form.validate():
        tour.time_requested = form.requestedDateTime.data

        if tour.last_requested == 'group':
            tour.last_requested = 'landlord'
        else:
            tour.last_requested = 'group'

        tour.genTimeChangeNotifications()

        session.commit()
    else:
        flash_errors(form)
        form.redirect()

    return redirect(url_for('tours.viewTour', tourID=tourID))


@tours.route('/tour/createMessage', methods=['POST'])
@login_required
@tour_viewable
def createMessage():
    form = TourMessageForm(request.form)

    if form.validate():
        tour = session.query(Tour).filter_by(id=form.tour_id.data).first_or_404()

        newTM = TourMessage(tour=tour,
                            content=form.content.data,
                            user=current_user)
        session.add(newTM)
        session.commit()

        newTM.genNotifications()

        return redirect(url_for('tours.viewTour', tourID=tour.id))
    else:
        flash_errors(form)

    return form.redirect()


@tours.route('/tour/<tourID>/decline/ajax')
@login_required
@tour_editable
def declineTourAJAX(tourID):
    tour = Tour.query.filter_by(id=tourID).first_or_404()

    tour.declined = True
    session.commit()

    tour.genDeniedNotifications()

    if request.is_xhr:
        return jsonify(results={'success': True})
    else:
        return redirect(url_for('tours.viewTour', tourID=tourID))


@tours.route('/tour/<tourID>/unDecline/ajax')
@login_required
@tour_editable
def unDeclineTourAJAX(tourID):
    tour = Tour.query.filter_by(id=tourID).first_or_404()
    tour.declined = False
    session.commit()

    tour.undoDeniedNotifications()

    if request.is_xhr:
        return jsonify(results={'success': True})
    else:
        return redirect(url_for('tours.viewTour', tourID=tourID))


@tours.route('/tour/<tourID>/getTourTimes')
@login_required
@tour_viewable
def getTourTimes(tourID):
    tour = Tour.query.filter_by(id=tourID).first_or_404()
    tourTimes = TourTime.query.filter_by(tour=tour).all()

    tourTimeList = []
    for tourTime in tourTimes:
        tourTimeList.append(tourTime.serialize)

    return jsonify({'tourTimes': tourTimeList})
