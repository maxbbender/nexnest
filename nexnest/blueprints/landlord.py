from flask import Blueprint, redirect, url_for, flash, render_template, jsonify, request, abort

from flask_login import login_required, current_user

from nexnest import db
from nexnest.models.landlord import Landlord
from nexnest.models.listing import Listing
from nexnest.models.landlord_listing import LandlordListing
from nexnest.models.availability import Availability
from nexnest.forms import TourDateChangeForm, PreCheckoutForm, LandlordPaymentAccountForm
from nexnest.utils.flash import flash_errors

from nexnest.static.dataSets import schoolUpgradePrice, summerUpgradePrice

from dateutil import parser

from pprint import pprint, pformat

from flask import current_app as app


landlords = Blueprint('landlords',
                      __name__,
                      template_folder='../templates/landlord')

session = db.session


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


@landlords.route('/landlord/dashboard/', defaults={'checkedFeaturedListingID': None})
@landlords.route('/landlord/dashboard/<int:checkedFeaturedListingID>')
@login_required
def landlordDashboard(checkedFeaturedListingID=None):
    if not current_user.landlord_info_filled:
        return redirect(url_for('users.landlordInformation'))

    dateChangeForm = TourDateChangeForm()
    landlord = session.query(Landlord) \
        .filter_by(user_id=current_user.id) \
        .first()

    nonFeaturedListings = []
    for listing in landlord.getListings():
        if not listing.featured:
            nonFeaturedListings.append(listing)

    checkedFeaturedListing = listing.query.filter_by(id=checkedFeaturedListingID).first()

    unAcceptedHousingRequests, acceptedHousingRequests, completedHousingRequests = landlord.getHousingRequests()
    openMaintenanceRequests, inProgressMaintenanceRequests, completedMaintenanceRequests = landlord.getMaintenanceRequests()
    currentHouses, futureHouses, unBookedHouses = landlord.getHouses()
    upcomingPayments, overduePayments, futurePayments, completedPayments = landlord.getGroupedRentPayments()

    requestedTours, scheduledTours = landlord.getActiveTours()

    return render_template('dashboard.html',
                           landlord=landlord,
                           dateChangeForm=dateChangeForm,
                           listings=landlord.getListings(checkedFeaturedListingID),
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
                           listingsToCheckout=nonFeaturedListings,
                           upcomingPayments=upcomingPayments,
                           overduePayments=overduePayments,
                           futurePayments=futurePayments,
                           completedPayments=completedPayments,
                           schoolUpgradePrice=schoolUpgradePrice,
                           summerUpgradePrice=summerUpgradePrice,
                           checkedFeaturedListingID=checkedFeaturedListingID,
                           checkedFeaturedListing=checkedFeaturedListing)


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


@landlords.route('/landlord/updateAvailability', methods=['POST'])
@login_required
def updateAvailability():
    landlord = Landlord.query.filter_by(user=current_user).first()

    if request.get_json() is not None:
        availabilityJSON = request.get_json(force=True)
        app.logger.debug('availabilityJSON %r' % availabilityJSON)

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


@landlords.route('/landlord/createPaymentAccount', methods=['GET', 'POST'])
@login_required
def createPaymentAcocunt():
    landlord = Landlord.query.filter_by(user=current_user).first_or_404()

    form = LandlordPaymentAccountForm(request.form)

    if form.validate_on_submit():
        app.logger.debug("Create Payment Account Form is Valid")
        braintreePayload = {}

        braintreeIndividual = {
            'first_name': landlord.user.fname,
            'last_name': landlord.user.lname,
            'email': landlord.user.email,
            'phone': landlord.user.phone,
            'date_of_birth': landlord.user.dob.strftime("%Y-%m-%d")
        }

        braintreeIndividual['address'] = {
            'street_address': landlord.street,
            'locality': landlord.city,
            'region': landlord.state,
            'postal_code': landlord.zip_code
        }

        braintreePayload['individual'] = braintreeIndividual

        if form.legalBusinessName.data != '':

            braintreePayload['business'] = {
                'legal_name': form.legalBusinessName.data,
                'tax_id': form.taxID.data
            }

        braintreePayload['funding'] = {
            'destination': 'bank',
            'account_number': form.accountNumber.data,
            'routing_number': form.routingNumber.data
        }

        app.logger.debug('Braintree Payload')
        app.logger.debug(pformat(braintreePayload))
    else:
        flash_errors(form)

    return render_template('paymentInformation.html',
                           form=form)
