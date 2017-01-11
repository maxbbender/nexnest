from flask import Blueprint
from flask import render_template, abort, request, redirect, url_for, flash, jsonify
from ..forms.listing import ListingForm

from nexnest.application import session

from nexnest.models.listing import Listing

from nexnest.utils.flash import flash_errors

listings = Blueprint('listings', __name__, template_folder='../templates')


@listings.route('/viewListing/<listingID>', methods=['GET', 'POST'])
def viewListing(listingID):
    # fake lisiting for testing
    viewListing = session.query(Listing).filter_by(id=listingID).first()
    return render_template('detailedListing.html', listing=viewListing, title='Listing')


@listings.route('/landlord/createListing', methods=['GET', 'POST'])
def createListing():
    form = ListingForm(request.form)
    if request.method == 'POST' and form.validate():
        newListing = Listing(street=form.street.data,
                             apartment_number=form.apartment_number.data,
                             city=form.city.data,
                             state=form.state.data,
                             zip_code=form.zip_code.data,
                             start_date=form.start_date.data,
                             end_date=form.end_date.data,
                             time_period=form.time_period.data,
                             unit_type=form.unit_type.data,
                             num_bedrooms=form.num_bedrooms.data,
                             num_full_baths=form.num_full_baths.data,
                             num_half_baths=form.num_half_baths.data,
                             price=form.price.data,
                             square_footage=form.square_footage.data,
                             parking=form.parking.data,
                             cats=form.cats.data,
                             dogs=form.dogs.data,
                             other_pets=form.other_pets.data,
                             washer=form.washer.data,
                             dryer=form.dryer.data,
                             dishwasher=form.dishwasher.data,
                             air_conditioning=form.air_conditioning.data,
                             handicap=form.handicap.data,
                             furnished=form.furnished.data,
                             utilities_included=form.utilities_included.data,
                             emergency_maintenance=form.emergency_maintenance.data,
                             snow_plowing=form.snow_plowing.data,
                             garbage_service=form.garbage_service.data,
                             security_service=form.security_service.data,
                             description=form.description.data)
        session.add(newListing)
        session.commit()
        flash('Listing Created')
        return redirect(url_for('indexs.index'))
    return render_template('/landlord/createListing.html', form=form, title='Create Listing')


@listings.route('/landlord/editListing/<listingID>', methods=['GET', 'POST'])
def editListing(listingID):
    form = ListingForm(request.form)
    currentListing = session.query(Listing).filter_by(id=listingID).first()
    if request.method == 'GET':
        print(currentListing.cats)
        form.street.data = currentListing.street
        form.city.data = currentListing.city
        form.zip_code.data = currentListing.zip_code
        form.start_date.data = currentListing.start_date
        form.end_date.data = currentListing.end_date
        form.time_period.data = currentListing.time_period
        form.unit_type.data = currentListing.unit_type
        form.apartment_number.data = currentListing.apartment_number
        form.num_bedrooms.data = currentListing.num_bedrooms
        form.num_full_baths.data = currentListing.num_full_baths
        form.num_half_baths.data = currentListing.num_half_baths
        form.price.data = currentListing.price
        form.square_footage.data = currentListing.square_footage
        form.parking.data = currentListing.parking
        form.cats.select = currentListing.cats
        form.dogs.select = currentListing.dogs
        form.other_pets.data = currentListing.other_pets
        form.washer.data = currentListing.washer
        form.dryer.data = currentListing.dryer
        form.dishwasher.data = currentListing.dishwasher
        form.air_conditioning.data = currentListing.air_conditioning
        form.handicap.data = currentListing.handicap
        form.furnished.data = currentListing.furnished
        form.utilities_included.data = currentListing.utilities_included
        form.emergency_maintenance.data = currentListing.emergency_maintenance
        form.snow_plowing.data = currentListing.snow_plowing
        form.garbage_service.data = currentListing.garbage_service
        form.security_service.data = currentListing.security_service
        form.description.data = currentListing.description
    if form.validate_on_submit():
        currentListing.street = form.street.data
        currentListing.city = form.city.data
        currentListing.zip_code = form.zip_code.data
        currentListing.start_date = form.start_date.data
        currentListing.end_date = form.end_date.data
        currentListing.time_period = form.time_period.data
        currentListing.unit_type = form.unit_type.data
        currentListing.apartment_number = form.apartment_number.data
        currentListing.num_bedrooms = form.num_bedrooms.data
        currentListing.num_full_baths = form.num_full_baths.data
        currentListing.num_half_baths = form.num_half_baths.data
        currentListing.price = form.price.data
        currentListing.square_footage = form.square_footage.data
        currentListing.parking = form.parking.data
        currentListing.cats = form.cats.data
        currentListing.dogs = form.dogs.data
        currentListing.other_pets = form.other_pets.data
        currentListing.washer = form.washer.data
        currentListing.dryer = form.dryer.data
        currentListing.dishwasher = form.dishwasher.data
        currentListing.air_conditioning = form.air_conditioning.data
        currentListing.handicap = form.handicap.data
        currentListing.furnished = form.furnished.data
        currentListing.utilities_included = form.utilities_included.data
        currentListing.emergency_maintenance = form.emergency_maintenance.data
        currentListing.snow_plowing = form.snow_plowing.data
        currentListing.garbage_service = form.garbage_service.data
        currentListing.security_service = form.security_service.data
        currentListing.description = form.description.data
        session.commit()
        flash('Listing Updated', 'info')
        return redirect(url_for('listing.viewListing', listingID=listingID))
    return render_template('/landlord/createListing.html', form=form, title='Edit Listing')
