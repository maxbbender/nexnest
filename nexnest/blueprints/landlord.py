from flask import Blueprint, redirect, url_for, flash, render_template, jsonify, request

from flask_login import login_required, current_user

from nexnest import logger
from nexnest.application import session
from nexnest.models.landlord import Landlord
from nexnest.models.listing import Listing
from nexnest.models.landlord_listing import LandlordListing
from nexnest.forms import TourDateChangeForm, PreCheckoutForm

landlords = Blueprint('landlords',
                      __name__,
                      template_folder='../templates/landlord')


@landlords.route('/landlord/dashboard')
@login_required
def landlordDashboard():
    dateChangeForm = TourDateChangeForm()
    if current_user.isLandlord:
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
    else:
        flash("You are not a landlord", 'warning')
        return redirect(url_for('indexs.index'))


@landlords.route('/landlord/requestedTours/JSON')
@login_required
def requestedToursJSON():
    if current_user.isLandlord:
        landlord = session.query(Landlord) \
            .filter_by(user_id=current_user.id) \
            .first()

        return jsonify(requestedTours=landlord.getRequestedToursJSON())
    else:
        return jsonify(requestedTours={'error': 'Invalid Permissions'})


@landlords.route('/landlord/scheduledTours/JSON')
@login_required
def scheduledToursJSON():
    if current_user.isLandlord:
        landlord = session.query(Landlord) \
            .filter_by(user_id=current_user.id) \
            .first()

        return jsonify(scheduledTours=landlord.getScheduledToursJSON())
    else:
        return jsonify(scheduledTours={'error': 'Invalid Permissions'})


@landlords.route('/landlord/unAcceptedGroupListings/JSON')
@login_required
def unAcceptedGroupListingsJSON():
    if current_user.isLandlord:
        landlord = session.query(Landlord) \
            .filter_by(user_id=current_user.id) \
            .first()

        return jsonify(unAcceptedGroupListings=landlord.getUnAcceptedGroupListingsJSON())
    else:
        return jsonify(unAcceptedGroupListings={'error': 'Invalid Permissions'})


@landlords.route('/landlord/acceptedGroupListings/JSON')
@login_required
def acceptedGroupListingsJSON():
    if current_user.isLandlord:
        landlord = session.query(Landlord) \
            .filter_by(user_id=current_user.id) \
            .first()

        return jsonify(acceptedGroupListings=landlord.getAcceptedGroupListingsJSON())
    else:
        return jsonify(acceptedGroupListings={'error': 'Invalid Permissions'})


@landlords.route('/landlord/openMaintenanceRequests/JSON')
@login_required
def openMaintenanceRequestsJSON():
    if current_user.isLandlord:
        landlord = session.query(Landlord) \
            .filter_by(user_id=current_user.id) \
            .first()

        return jsonify(openMaintenanceRequests=landlord.getOpenMaintenanceJSON())
    else:
        return jsonify(openMaintenanceRequests={'error': 'Invalid Permissions'})


@landlords.route('/landlord/inProgressMaintenanceRequests/JSON')
@login_required
def inProgressMaintenanceRequestsJSON():
    if current_user.isLandlord:
        landlord = session.query(Landlord) \
            .filter_by(user_id=current_user.id) \
            .first()

        return jsonify(inProgressMaintenanceRequests=landlord.getInProgressMaintenanceJSON())
    else:
        return jsonify(inProgressMaintenanceRequests={'error': 'Invalid Permissions'})


@landlords.route('/landlord/completedMaintenanceRequests/JSON')
@login_required
def completedMaintenanceRequestsJSON():
    if current_user.isLandlord:
        landlord = session.query(Landlord) \
            .filter_by(user_id=current_user.id) \
            .first()

        return jsonify(completedMaintenanceRequests=landlord.getCompletedMaintenanceJSON())
    else:
        return jsonify(completedMaintenanceRequests={'error': 'Invalid Permissions'})


@landlords.route('/landlord/unBookedHouses/JSON')
@login_required
def unBookedHousesJSON():
    if current_user.isLandlord:
        landlord = session.query(Landlord) \
            .filter_by(user_id=current_user.id) \
            .first()

        return jsonify(unBookedHouses=landlord.getUnBookedHousesJSON())
    else:
        return jsonify(unBookedHouses={'error': 'Invalid Permissions'})


@landlords.route('/landlord/<listingID>/isEditable/AJAX')
@login_required
def isEditable(listingID):
    listing = session.query(Listing).filter_by(id=listingID).first()

    if listing.isEditableBy(current_user):
        return jsonify(results={'success': True})
    else:
        return jsonify(results={'success': False, 'message': 'Permissions Error'})


@landlords.route('/landlord/updateAvailability', methods=['POST'])
@login_required
def updateAvailability():
    print('JSONFIFIFIF %r' % request.get_json())
    availabilityJSON = request.get_json(force=True)
    logger.debug('RecievedJSON %r' % availabilityJSON)
    return jsonify({'success': True})
