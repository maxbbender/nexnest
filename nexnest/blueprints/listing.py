import os
import json

from flask import Blueprint
from flask import render_template, request, redirect, url_for, flash
from flask_login import current_user, login_required
from werkzeug import secure_filename  # pylint: disable=E0611

from nexnest import logger
from nexnest.application import session, app

from nexnest.forms import ListingForm, SuggestListingForm, TourForm, GroupListingForm
from nexnest.models.listing import Listing
from nexnest.models.listing_school import ListingSchool
from nexnest.models.landlord_listing import LandlordListing
from nexnest.models.school import School

from nexnest.utils.flash import flash_errors
from nexnest.utils.file import allowed_file, isPDF
from nexnest.utils.school import allSchoolsAsStrings

listings = Blueprint('listings', __name__, template_folder='../templates')


@listings.route('/listing/view/<listingID>', methods=['GET', 'POST'])
@login_required
def viewListing(listingID):
    listing = session.query(Listing).filter_by(id=listingID).first()
    myGroups = current_user.accepted_groups
    return render_template('detailedListing.html',
                           suggestListingForm=SuggestListingForm(),
                           requestTourForm=TourForm(),
                           requestListingForm=GroupListingForm(),
                           listing=listing,
                           groups=myGroups,
                           title='Listing',
                           pictures=listing.getPhotoURLs())


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
                                     emergency_maintenance=form.emergency_maintenance.data,
                                     snow_plowing=form.snow_plowing.data,
                                     garbage_service=form.garbage_service.data,
                                     security_service=form.security_service.data,
                                     description=form.description.data,
                                     num_full_baths=form.num_full_baths.data,
                                     num_half_baths=form.num_half_baths.data,
                                     time_period=form.time_period.data,
                                     rent_due=form.rent_due.data,
                                     property_type=form.property_type.data,
                                     electricity=form.electricity.data,
                                     internet=form.internet.data,
                                     water=form.water.data,
                                     heat_gas=form.heat_gas.data,
                                     cable=form.cable.data,
                                     washer_free=form.washer_free.data,
                                     youtube_url=form.youtube_url.data)

                session.add(newListing)
                session.commit()

                # Now we want to define the colleges this listing is associated with

                collegeNames = json.loads(form.colleges.data)

                for collegeName in collegeNames:
                    school = session.query(School).filter_by(name=collegeName).first()

                    if school is not None:
                        newListingSchool = ListingSchool(listing=newListing, school=school)
                        session.add(newListingSchool)
                        session.commit()
                        logger.debug('newListingSchool %r' % newListingSchool)
                    else:
                        logger.error('Could not find school with name %s. Could not associated listing %r with school' % (collegeName, newListing))

                logger.debug('form.colleges.data : %s' % form.colleges.data)
                logger.debug('collegeNames %r' % collegeNames)

                if newListing.property_type == 'apartment':
                    newListing.apartment_number = form.apartment_number.data

                if newListing.rent_due == 'semester':
                    newListing.first_semester_rent_due_date = form.first_semester_rent_due_date.data
                    newListing.second_semester_rent_due_date = form.second_semester_rent_due_date.data

                session.commit()

                # Let's create the folder to upload the photos to.
                folderPath = os.path.join(app.config['UPLOAD_FOLDER'], 'listings', str(newListing.id))

                if not os.path.exists(folderPath):
                    os.makedirs(folderPath)

                folderPicturesPath = os.path.join(folderPath, 'pictures')
                if not os.path.exists(folderPicturesPath):
                    os.makedirs(folderPicturesPath)

                # Lets add the photos
                uploadedFiles = request.files.getlist("pictures")

                if not uploadedFiles[0].filename == '':
                    logger.debug("Uploaded Files : %r" % uploadedFiles)
                    filenames = []
                    fileUploadError = False
                    for file in uploadedFiles:
                        if file and allowed_file(file.filename):
                            filename = secure_filename(file.filename)

                            file.save(os.path.join(folderPicturesPath, filename))
                            filenames.append(filename)
                        else:
                            fileUploadError = True
                            logger.error("Error saving file %s" % file.filename)

                    if fileUploadError:
                        flash("Error saving file", 'danger')
                else:
                    logger.debug("No Picture files to upload")

                flash('Listing Created', 'success')

                if 'floor_plan' in request.files:
                    file = request.files['floor_plan']

                    if file and isPDF(file.filename):
                        filename = secure_filename(request.files['floor_plan'].filename)

                        if file and allowed_file(filename):
                            # print('Trying to save file in %s' % os.path.join(folderPath, 'floorplan.pdf'))
                            file.save(os.path.join(folderPath, 'floorplan.pdf'))

                    newListing.floor_plan_url = os.path.join(folderPath, 'floorplan.pdf')
                    newListing.floor_plan_url = '/uploads/listings/%s/floorplan.pdf' % str(newListing.id)

                    session.commit()

                return redirect(url_for('listings.viewListing', listingID=newListing.id))
            else:
                flash_errors(form)
                return render_template('/landlord/createListing.html',
                                       form=form,
                                       title='Create Listing',
                                       schools=allSchoolsAsStrings())
        else:
            form = ListingForm()
            return render_template('/landlord/createListing.html',
                                   form=form,
                                   title='Create Listing',
                                   schools=allSchoolsAsStrings()
                                   )
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


# @listings.route('/listing/search/AJAX', methods=['POST'])
# def searchListingsAJAX():
#     # json = request.get_json(force=True)
#     postedJSON = {
#         'bedrooms': 4,  # 1-4 (if at 4 it means 4+)
#         'distanceToCampus': 8,  # In miles
#         'includes': [  # If any of these are here this means that they are check, if not they are not checked. If they are check the listing HAS to have them. if not don't add to filter
#             'furnished',
#             'dishwasher',
#             'laundry',
#             'internet',
#             'cable',
#             'snowRemoval',
#             'garbageRemoval'
#         ],
#         'listingTypes': [  # Only show if element of list, don't show if not element
#             'house',
#             'apartment',
#             'complex'
#         ],
#         'school': 'Marist',  # This will be switched to school
#         'minPrice': 1000,
#         'maxPrice': 3000,
#         'pets': [  # Same as includes
#             'dogs',
#             'cats'
#         ],
#         'priceTerm': 'month',  # month|semester (based on listing price) MATHS
#         'sortBy': None,  # priceLowToHigh|priceHighToLow|mostRecent|distanceToCampus
#         'term': '2018-2019 School Year'  # YYYY-YYYY [School Year|Summer]

#     }
#     # Required Fields : bedrooms  | minPrice | maxPrice | €22
#     allListings = None
#     # Bedroom Checks:
#     if 'bedrooms' in postedJSON:
#         if postedJSON['bedrooms'] < 4:
#             allListings = session.query(Listing).fitler(Listing.num_bedrooms == postedJSON['bedrooms'])
#         else:
#             allListings = session.query(Listing).fitler(Listing.num_bedrooms >= 4)

#     if 'minPrice' in postedJSON:
#         if allListings.filter(Listing.)


#     # sortBy Check
#     if ['sortBy'] in postedJSON:
#         if postedJSON['sortBy'] == 'priceLowToHigh':

#         elif postedJSON['sortBy'] == 'priceHighToLow':

#         elif postedJSON['sortBy'] == 'mostRecent':

#         elif postedJSON['sortBy'] == 'distanceToCampus':

#             # No sorting
#     else:

#     if postedJSON['bedrooms'] < 4:

#     return {
#         'distance': {
#             'school': {
#                 'name'
#             }
#         }
#     }
