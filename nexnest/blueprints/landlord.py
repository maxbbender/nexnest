from flask import Blueprint, redirect, url_for, flash, render_template, jsonify, request, abort

from flask_login import login_required, current_user

from nexnest import logger
from nexnest.application import session
from nexnest.models.landlord import Landlord
from nexnest.models.listing import Listing
from nexnest.models.landlord_listing import LandlordListing
from nexnest.models.availability import Availability
from nexnest.forms import TourDateChangeForm, PreCheckoutForm

from dateutil import parser

landlords = Blueprint('landlords',
                      __name__,
                      template_folder='../templates/landlord')


@landlords.before_request
def isLandlord():
    if not current_user.is_authenticated:
        if request.is_xhr:
            return jsonify({'success': False, 'message': 'Permissions Error'})
        else:
            abort(403)

    if not current_user.isLandlord:
        if request.is_xhr:
            return jsonify({'success': False, 'message': 'Permissions Error'})
        else:
            abort(403)


@landlords.route('/landlord/dashboard')
@login_required
def landlordDashboard():
    dateChangeForm = TourDateChangeForm()
    landlord = session.query(Landlord) \
        .filter_by(user_id=current_user.id) \
        .first()

    nonActiveListings = []
    for listing in landlord.getListings():
        if not listing.active:
            nonActiveListings.append(listing)

    unAcceptedHousingRequests, acceptedHousingRequests, completedHousingRequests = landlord.getHousingRequests()
    openMaintenanceRequests, inProgressMaintenanceRequests, completedMaintenanceRequests = landlord.getMaintenanceRequests()
    currentHouses, futureHouses, unBookedHouses = landlord.getHouses()

    requestedTours, scheduledTours = landlord.getActiveTours()

    return render_template('dashboard.html',
                           landlord=landlord,
                           dateChangeForm=dateChangeForm,
                           listings=landlord.getListings(),
                           requestedTours=requestedTours,
                           scheduledTours=scheduledTours,
                           unAcceptedHousingRequests=unAcceptedHousingRequests,
                           acceptedHousingRequests=acceptedHousingRequests,
                           completedHousingRequests=completedHousingRequests,
                           currentHouses=currentHouses,
                           futureHouses=futureHouses,
                           unBookedHouses=unBookedHouses,
                           openMaintenanceRequests=openMaintenanceRequests,
                           inProgressMaintenanceRequests=inProgressMaintenanceRequests,
                           completedMaintenanceRequests=completedMaintenanceRequests,
                           preCheckoutForm=PreCheckoutForm(),
                           listingsToCheckout=nonActiveListings)


@landlords.route('/landlord/requestedTours/JSON')
@login_required
def requestedToursJSON():
    landlord = session.query(Landlord) \
        .filter_by(user_id=current_user.id) \
        .first()

    return jsonify(requestedTours=landlord.getRequestedToursJSON())


@landlords.route('/landlord/scheduledTours/JSON')
@login_required
def scheduledToursJSON():
    landlord = session.query(Landlord) \
        .filter_by(user_id=current_user.id) \
        .first()

    return jsonify(scheduledTours=landlord.getScheduledToursJSON())


@landlords.route('/landlord/unAcceptedGroupListings/JSON')
@login_required
def unAcceptedGroupListingsJSON():
    landlord = session.query(Landlord) \
        .filter_by(user_id=current_user.id) \
        .first()

    return jsonify(unAcceptedGroupListings=landlord.getUnAcceptedGroupListingsJSON())


@landlords.route('/landlord/acceptedGroupListings/JSON')
@login_required
def acceptedGroupListingsJSON():
    landlord = session.query(Landlord) \
        .filter_by(user_id=current_user.id) \
        .first()

    return jsonify(acceptedGroupListings=landlord.getAcceptedGroupListingsJSON())


@landlords.route('/landlord/openMaintenanceRequests/JSON')
@login_required
def openMaintenanceRequestsJSON():
    landlord = session.query(Landlord) \
        .filter_by(user_id=current_user.id) \
        .first()

    return jsonify(openMaintenanceRequests=landlord.getOpenMaintenanceJSON())


@landlords.route('/landlord/inProgressMaintenanceRequests/JSON')
@login_required
def inProgressMaintenanceRequestsJSON():
    landlord = session.query(Landlord) \
        .filter_by(user_id=current_user.id) \
        .first()

    return jsonify(inProgressMaintenanceRequests=landlord.getInProgressMaintenanceJSON())


@landlords.route('/landlord/completedMaintenanceRequests/JSON')
@login_required
def completedMaintenanceRequestsJSON():
    landlord = session.query(Landlord) \
        .filter_by(user_id=current_user.id) \
        .first()

    return jsonify(completedMaintenanceRequests=landlord.getCompletedMaintenanceJSON())


@landlords.route('/landlord/unBookedHouses/JSON')
@login_required
def unBookedHousesJSON():
    landlord = session.query(Landlord) \
        .filter_by(user_id=current_user.id) \
        .first()

    return jsonify(unBookedHouses=landlord.getUnBookedHousesJSON())


@landlords.route('/landlord/<listingID>/isEditable/AJAX')
@login_required
def isEditable(listingID):
    listing = session.query(Listing).filter_by(id=listingID).first()

    if listing.isEditableBy(current_user):
        return jsonify(results={'success': True})
    else:
        return jsonify(results={'success': False, 'message': 'Permissions Error'})


@landlords.route('/landlord/updateAvailability/', methods=['POST'])
@login_required
def updateAvailability():
    landlord = Landlord.query.filter_by(user=current_user).first()

    if request.get_json() is not None:
        availabilityJSON = request.get_json(force=True)
        logger.debug('availabilityJSON %r' % availabilityJSON)

        # Remove current availability
        Availability.query.filter_by(landlord=landlord).delete()

        # daysOfWeek = ['sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday']

        for i in range(7):
            day = str(i)
            if day in availabilityJSON:
                if len(availabilityJSON[day]) > 0:
                    for time in availabilityJSON[day]:
                        time = parser.parse(time).time()
                        newAvailability = Availability(landlord, time, day)
                        session.add(newAvailability)
                        session.commit()

        return jsonify({'success': True})
    else:
        return jsonify({'success': False, 'message': 'Invalid Request (JSON is None)'})


@landlords.route('/landlord/getAvailability/JSON/<landlordID>', methods=['GET'])
@login_required
def getAvailability(landlordID=None):
    if landlordID is None:
        landlordID = current_user.id

    availabilityList = []

    for i in range(7):
        availabilities = Availability.query \
            .filter_by(landlord_id=landlordID, day=i) \
            .order_by(Availability.time.asc()) \
            .all()

        for avail in availabilities:
            availabilityList.append(avail.serialize)

    return jsonify(availabilityList)
