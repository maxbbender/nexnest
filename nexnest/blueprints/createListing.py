from flask import Blueprint
from flask import render_template, abort, request, redirect, url_for, flash, jsonify
from ..forms.createListing import CreateListingForm

from nexnest.application import session

from nexnest.models.listing import Listing

from nexnest.utils.flash import flash_errors

createListings = Blueprint('createListings', __name__, template_folder='../templates')

@createListings.route('/landlord/createListing', methods=['GET', 'POST'])
def createListing():
    form = CreateListingForm(request.form)
    if request.method == 'POST' and form.validate():
        newListing = Listing(street=form.street.data, 
                            city=form.city.data, 
                            state=form.state.data,
                            zip_code=form.zip_code.data,
                            start_date=form.start_date.data,
                            end_date=form.end_date.data,
                            unit_type=form.unit_type.data,
                            num_bedrooms=form.num_bedrooms.data,
                            #num_full_baths=form.start_date.data,
                            #num_half_baths=form.start_date.data,
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
                            security_service=form.security_service.data)
                            #description=form.start_date.data
        session.add(newListing)
        session.commit()
        flash('Listing Created')
        return redirect(url_for('indexs.index'))
    return render_template('/landlord/createListing.html', form=form, title='Create Listing')