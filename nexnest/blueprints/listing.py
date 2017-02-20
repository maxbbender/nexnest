from flask import Blueprint
from flask import render_template, request, redirect, url_for, flash
from flask_login import current_user, login_required

from nexnest.application import session, app

from nexnest.forms import ListingForm, SuggestListingForm, TourForm, GroupListingForm
from nexnest.models.listing import Listing
from nexnest.models.landlord_listing import LandlordListing

from nexnest.utils.flash import flash_errors
from nexnest.utils.file import allowed_file

import os

from werkzeug import secure_filename

listings = Blueprint('listings', __name__, template_folder='../templates')


@listings.route('/listing/view/<listingID>', methods=['GET', 'POST'])
@login_required
def viewListing(listingID):
    viewListing = session.query(Listing).filter_by(id=listingID).first()
    myGroups = current_user.accepted_groups
    return render_template('detailedListing.html',
                           suggestListingForm=SuggestListingForm(),
                           requestTourForm=TourForm(),
                           requestListingForm=GroupListingForm(),
                           listing=viewListing,
                           groups=myGroups,
                           title='Listing')


@listings.route('/listing/create', methods=['GET', 'POST'])
@login_required
def createListing():
    # User can only create listing if landlord
    if current_user.isLandlord:
        if request.method == 'POST':
            form = ListingForm(request.form)
            print(form)
            if form.validate():
                newListing = Listing(street=form.street.data,
                                     city=form.city.data,
                                     state=form.state.data,
                                     zip_code=form.zip_code.data,
                                     start_date=form.start_date.data,
                                     end_date=form.end_date.data,
                                     num_bedrooms=form.num_bedrooms.data,
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
                                     description=form.description.data,
                                     num_full_baths=form.num_full_baths.data,
                                     num_half_baths=form.num_half_baths.data,
                                     time_period=form.time_period.data,
                                     rent_due=form.rent_due.data,
                                     property_type=form.property_type.data)
                session.add(newListing)
                session.commit()

                if newListing.property_type == 'apartment':
                    newListing.apartment_number = form.apartment.data

                if newListing.rent_due == 'semester':
                    newListing.first_semester_rent_due_date = form.first_semester_rent_due_date.data
                    newListing.second_semester_rent_due_date = form.second_semester_rent_due_date.data
                else:
                    newListing.monthly_rent_due_date = form.monthly_rent_due_date.data

                session.commit()

                # Let's create the folder to upload the photos to.
                folderPath = os.path.join(app.config['UPLOAD_FOLDER'], 'listings', str(newListing.id))

                if not os.path.exists(folderPath):
                    os.makedirs(folderPath)

                # Lets add the photos
                print(request.files.getlist("pictures"))
                print(request.files.getlist("pictures"))
                uploadedFiles = request.files.getlist("pictures")
                print(uploadedFiles)
                filenames = []
                for file in uploadedFiles:
                    print ('hey')
                    if file and allowed_file(file.filename):
                        filename = secure_filename(file.filename)

                        file.save(os.path.join(folderPath, filename))
                        filenames.append(filename)

                print(filenames)

                flash('Listing Created', 'success')
                return redirect(url_for('indexs.index'))
            else:
                flash_errors(form)
                return render_template('/landlord/createListing.html',
                                       form=form,
                                       title='Create Listing')
        else:
            form = ListingForm()
            return render_template('/landlord/createListing.html',
                                   form=form,
                                   title='Create Listing')
    else:
        flash("Only Landlords can create listings", 'warning')
        return redirect(url_for('indexs.index'))


@listings.route('/listing/edit/<listingID>', methods=['GET', 'POST'])
@login_required
def editListing(listingID):
    listingLandlords = session.query(LandlordListing) \
        .filter_by(listing_id=listingID,
                   landlord_id=current_user.id) \
        .count()

    # The current user is a landlord for this listing
    if listingLandlords > 0:

        currentListing = session.query(
            Listing).filter_by(id=listingID).first()

        form = ListingForm(obj=currentListing,
                           unit_type=currentListing.unit_type,
                           time_period=currentListing.time_period,
                           parking=currentListing.parking)

        if request.method == 'GET':
            return render_template('/landlord/createListing.html',
                                   form=form,
                                   title='Edit Listing')
        else:  # POST
            form = ListingForm(request.form)

            if form.validate():
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
                return redirect(url_for('listings.viewListing',
                                        listingID=listingID))
    else:
        flash("You are not the landlord of this listing", 'warning')

        return redirect(url_for('listings.viewListing',
                                listingID=listingID))
