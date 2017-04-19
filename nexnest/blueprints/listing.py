import os
import json
import re
import datetime

from flask import Blueprint
from flask import render_template, request, redirect, url_for, flash, jsonify
from flask_login import current_user, login_required
from werkzeug import secure_filename  # pylint: disable=E0611

from sqlalchemy import or_

from nexnest import logger
from nexnest.application import session, app, csrf

from nexnest.forms import ListingForm, SuggestListingForm, TourForm, GroupListingForm, PhotoForm
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
    logger.debug('/listing/create createListing()')
    # User can only create listing if landlord
    if current_user.isLandlord:
        if request.method == 'POST':
            form = ListingForm(request.form)
            logger.debug('POST form : %r' % form)
            logger.debug('TimePeriodDateRange : %s' % form.time_period_date_range.data)
            logger.debug('Start Date : %r' % form.start_date.data)
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
                                     time_period_date_range=form.time_period_date_range.data,
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
                                     youtube_url=form.youtube_url.data,
                                     first_semester_rent_due_date=form.first_semester_rent_due_date.data,
                                     second_semester_rent_due_date=form.second_semester_rent_due_date.data)

                otherListingsWithSameAddress = session.query(Listing) \
                    .filter_by(street=newListing.street,
                               city=newListing.city,
                               state=newListing.state,
                               zip_code=newListing.zip_code,
                               ) \
                    .all()

                conflictingDates = False
                conflictingListing = None
                for listing in otherListingsWithSameAddress:
                    newListingStartDate = datetime.datetime.strptime(newListing.start_date, "%Y-%m-%d").date()
                    newListingEndDate = datetime.datetime.strptime(newListing.end_date, "%Y-%m-%d").date()
                    if newListingStartDate <= listing.end_date and newListingStartDate >= listing.start_date:
                        conflictingListing = listing
                        conflictingDates = True
                        break
                    elif newListingStartDate <= listing.start_date and newListingEndDate >= listing.start_date:
                        conflictingListing = listing
                        conflictingDates = True
                        break

                if not conflictingDates:

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
                    return redirect(url_for('listings.uploadPhotos', listingID=newListing.id))

                else:
                    flash('There is conflicting dates with a listing at the same address. \nThe conflicting listing is listed from %s - %s' %
                          (conflictingListing.start_date.strftime("%B %d, %Y"),
                           conflictingListing.end_date.strftime("%B %d, %Y")), 'warning')
                    return render_template('/landlord/createListing.html',
                                           form=form,
                                           title='Create Listing',
                                           schools=allSchoolsAsStrings())
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


@listings.route('/listing/clone/<listingID>', methods=['GET', 'POST'])
@login_required
def cloneListing(listingID):
    listingLandlords = session.query(LandlordListing) \
        .filter_by(listing_id=listingID,
                   landlord_id=current_user.id) \
        .count()

    # The current user is a landlord for this listing
    if listingLandlords > 0:

        currentListing = session.query(
            Listing).filter_by(id=listingID).first()

        # Get colleges associated with the listing
        selectedSchools = session.query(ListingSchool).filter_by(listing=currentListing).all()

        #Get the previous pictures
        folderPath = os.path.join(app.config['UPLOAD_FOLDER'], 'listings', str(listingID))
        folderPicturesPath = os.path.join(folderPath, 'pictures')
        picturePaths = os.listdir(folderPicturesPath)

        form = ListingForm(obj=currentListing)
        return render_template('/landlord/createListing.html',
                               form=form,
                               title='Create Listing',
                               schools=allSchoolsAsStrings(),
                               selectedSchools=selectedSchools,
                               picturePaths=picturePaths)
    else:
        flash("You are not the landlord of this listing", 'warning')

        return redirect(url_for('listings.viewListing',
                                listingID=listingID))


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

        # Get colleges associated with the listing
        selectedSchools = session.query(ListingSchool).filter_by(listing=currentListing).all()

        #Get the pictures from the liting
        folderPath = os.path.join(app.config['UPLOAD_FOLDER'], 'listings', str(listingID))
        folderPicturesPath = os.path.join(folderPath, 'pictures')
        picturePaths = os.listdir(folderPicturesPath)

        #Get the bannerPhoto from the liting
        # bannerFolderPath = os.path.join(app.config['UPLOAD_FOLDER'], 'listings', str(listingID))
        # bannerFolderPicturesPath = os.path.join(bannerFolderPath, 'bannerPhoto')
        # bannerPath = os.listdir(bannerFolderPicturesPath)

        form = ListingForm(obj=currentListing)

        if request.method == 'GET':
            return render_template('/landlord/editListing.html',
                                   form=form,
                                   title='Edit Listing',
                                   listingID=listingID,
                                   schools=allSchoolsAsStrings(),
                                   selectedSchools=selectedSchools,
                                   picturePaths=picturePaths)
        else:  # POST
            form = ListingForm(request.form)

            if form.validate():
                currentListing.street = form.street.data
                currentListing.city = form.city.data
                currentListing.state = form.state.data
                currentListing.zip_code = form.zip_code.data
                currentListing.start_date = form.start_date.data
                currentListing.end_date = form.end_date.data
                currentListing.time_period = form.time_period.data
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
                currentListing.emergency_maintenance = form.emergency_maintenance.data
                currentListing.snow_plowing = form.snow_plowing.data
                currentListing.garbage_service = form.garbage_service.data
                currentListing.security_service = form.security_service.data
                currentListing.description = form.description.data
                currentListing.rent_due = form.rent_due.data
                currentListing.property_type = form.property_type.data
                currentListing.electricity = form.electricity.data
                currentListing.internet = form.internet.data
                currentListing.water = form.water.data
                currentListing.heat_gas = form.heat_gas.data
                currentListing.cable = form.cable.data
                currentListing.washer_free = form.washer_free.data
                currentListing.youtube_url = form.youtube_url.data
                if form.property_type == 'apartment':
                    currentListing.apartment_number = form.apartment_number.data

                if form.rent_due == 'semester':
                    currentListing.first_semester_rent_due_date = form.first_semester_rent_due_date.data
                    currentListing.second_semester_rent_due_date = form.second_semester_rent_due_date.data
                session.commit()

                folderPath = os.path.join(app.config['UPLOAD_FOLDER'], 'listings', str(listingID))
                if not os.path.exists(folderPath):
                    os.makedirs(folderPath)

                folderPicturesPath = os.path.join(folderPath, 'bannerPhoto')
                if not os.path.exists(folderPicturesPath):
                    os.makedirs(folderPicturesPath)

                # Lets add the photos
                uploadedFiles = request.files.getlist("bannerPicture")
                filenames = []
                for file in uploadedFiles:
                    if file and allowed_file(file.filename):
                        extension = os.path.splitext(file.filename)[1]
                        filename = "listing"+listingID+"banner"+extension

                        file.save(os.path.join(folderPicturesPath, filename))
                        filenames.append(filename)
                    else:
                        flash("Error saving file %s" % file.filename, 'error')
                flash('Listing Updated', 'info')
                return redirect(url_for('listings.viewListing',
                                        listingID=listingID))
            else:
                flash_errors(form)
                return render_template('/landlord/editListing.html',
                                       form=form,
                                       title='Edit Listing',
                                       listingID=listingID,
                                       schools=allSchoolsAsStrings(),
                                       selectedSchools=selectedSchools,
                                       picturePaths=picturePaths)
    else:
        flash("You are not the landlord of this listing", 'warning')

        return redirect(url_for('listings.viewListing',
                                listingID=listingID))


@app.route("/listing/upload/<listingID>", methods=["POST"])
@csrf.exempt
def upload(listingID):
    """Handle the upload of a file."""

    # Is the upload using Ajax, or a direct POST by the form?
    is_ajax = True

    # Target folder for these uploads.
    #target = "/uploads/listings/11/pictures"
    folderPath = os.path.join(app.config['UPLOAD_FOLDER'], 'listings', str(listingID))
    try:
        if not os.path.exists(folderPath):
            os.makedirs(folderPath)

        folderPicturesPath = os.path.join(folderPath, 'pictures')
        if not os.path.exists(folderPicturesPath):
            os.makedirs(folderPicturesPath)
    except:
        if is_ajax:
            logger.error(False, "Couldn't create upload directory: {}".format(folderPicturesPath))
        else:
            return "Couldn't create upload directory: {}".format(folderPicturesPath)
    for upload in request.files.getlist("pictures"):
        extension = os.path.splitext(upload.filename)[1]
        #filename = upload.filename.rsplit("/")[0]
        dir = folderPicturesPath
        list = os.listdir(dir) # dir is your directory path
        number_files = len(list)
        filename = "listing"+listingID+"photo"+str(number_files)+extension
        logger.debug(number_files)
        logger.debug("filename is " + filename)
        destination = "/".join([folderPicturesPath, filename])
        upload.save(destination)

    if is_ajax:
        logger.debug(True, folderPicturesPath)
        return jsonify("hello");
    else:
        return redirect(url_for("upload_complete", uuid=folderPicturesPath))

@app.route("/listing/delete/<listingID>/<filename>", methods=["POST"])
@csrf.exempt
def deletePhoto(listingID, filename):
    folderPath = os.path.join(app.config['UPLOAD_FOLDER'], 'listings', str(listingID))
    folderPicturesPath = os.path.join(folderPath, 'pictures')
    os.remove(folderPicturesPath+"/"+filename)
    return jsonify("hello");

@listings.route('/listing/<listingID>/uploadPhotos', methods=['GET', 'POST'])
@login_required
def uploadPhotos(listingID):
    if current_user.isLandlord:
        if request.method == 'POST':
            form = PhotoForm(request.form)
            if form.validate():
                #upload the banner folder
                folderPath = os.path.join(app.config['UPLOAD_FOLDER'], 'listings', str(listingID))
                if not os.path.exists(folderPath):
                    os.makedirs(folderPath)

                folderPicturesPath = os.path.join(folderPath, 'bannerPhoto')
                if not os.path.exists(folderPicturesPath):
                    os.makedirs(folderPicturesPath)

                # Lets add the photos
                uploadedFiles = request.files.getlist("bannerPicture")
                filenames = []
                for file in uploadedFiles:
                    if file and allowed_file(file.filename):
                        extension = os.path.splitext(file.filename)[1]
                        filename = "listing"+listingID+"banner"+extension

                        file.save(os.path.join(folderPicturesPath, filename))
                        filenames.append(filename)
                    else:
                        flash("Error saving file %s" % file.filename, 'error')
                flash('Listing Created', 'success')
                if form.nextAction.data == 'checkout':
                    return redirect(url_for('landlords.landlordDashboard'))
                elif form.nextAction.data == 'createNew':
                    return redirect(url_for('listings.createListing'))
                elif form.nextAction.data == 'createCopy':
                    selectedSchools = session.query(ListingSchool).filter_by(listing=listingID).all()
                    #Get Pictures
                    return render_template('/landlord/createListing.html',
                                           form=form,
                                           title='Create Listing',
                                           schools=allSchoolsAsStrings(),
                                           selectedSchools=selectedSchools)
                return jsonify("Only reach here if you somehow messed up the nextAction");
            else:
                return jsonify("Do something Smart Here");
        else:
            form = PhotoForm()
            return render_template('/landlord/uploadPhotos.html',
                                   form=form,
                                   title='Upload Photos',
                                   listingID=listingID
                                   )
    else:
        flash("Only Landlords can upload photos", 'warning')
        return redirect(url_for('indexs.index'))


@listings.route('/listing/search/AJAX', methods=['POST', 'GET'])
@csrf.exempt
def searchListingsAJAX():
    logger.debug("@listings.route('/listing/search/AJAX")
    postedJSON = request.get_json(force=True)
    # postedJSON = {
    #     'bedrooms': 3,  # 1-4 (if at 4 it means 4+)
    #     # 'distanceToCampus': 8,  # In miles
    #     'includes': [  # If any of these are here this means that they are check, if not they are not checked. If they are check the listing HAS to have them. if not don't add to filter
    #         # 'furnished',
    #         # 'dishwasher',
    #         # 'laundry',
    #         # 'internet',
    #         # 'cable',
    #         # 'snowRemoval',
    #         # 'garbageRemoval'
    #     ],
    #     'listingTypes': [  # Only show if element of list, don't show if not element
    #         'house',
    #         'apartment',
    #         'complex'
    #     ],
    #     'school': 'Marist',  # This will be switched to school
    #     'minPrice': 1000,
    #     'maxPrice': 3000,
    #     'pets': [  # Same as includes
    #         # 'dogs',
    #         # 'cats'
    #     ],
    #     'sortBy': None,  # priceLowToHigh|priceHighToLow|mostRecent|distanceToCampus
    #     'term': '2017-2018 School Year'  # YYYY-YYYY [School Year|Summer]

    # }
    # Required Fields : `bedrooms` | `minPrice` | `maxPrice` | `priceTerm` | `school`
    allListings = session.query(Listing).filter(Listing.active)

    # Bedroom Checks:
    if 'bedrooms' in postedJSON:
        if postedJSON['bedrooms'] < 4:
            allListings = allListings.filter(Listing.num_bedrooms == postedJSON['bedrooms'])
        else:
            allListings = allListings.filter(Listing.num_bedrooms >= 4)
    else:
        logger.error("Bedrooms not found in listing search query")

    logger.debug("Bedrooms allListings %r" % allListings.all())

    # Price Checks
    if 'minPrice' in postedJSON and 'maxPrice' in postedJSON:
        allListings = allListings.filter(Listing.price_per_month >= postedJSON['minPrice'], Listing.price_per_month <= postedJSON['maxPrice'])
    else:
        logger.error('Minimum or Maximum price not found in listing search query')

    logger.debug("Price allListings %r" % allListings.all())

    # Term Checks
    if 'term' in postedJSON:
        schoolYearPattern = re.compile(r"(\d{4}-\d{4})")
        match = schoolYearPattern.match(postedJSON['term'])
        if match:
            allListings = allListings.filter(Listing.time_period_date_range == match.group(1),
                                             or_(Listing.time_period == 'school',
                                                 Listing.time_period == 'year'))
        else:
            summerPattern = re.compile(r"(\d{4}) Summer")
            match = summerPattern.match(postedJSON['term'])

            if match:
                allListings = allListings.filter(Listing.time_period_date_range == match.group(1),
                                                 Listing.time_period == 'summer')
            else:
                logger.error("term input is invalid and does not match any patterns defined. postedJSON['term'] : %s" % postedJSON['term'])
    else:
        logger.error("Term not found in listing search query")

    logger.debug("Term allListings %r" % allListings.all())

    # School
    if 'school' in postedJSON:
        logger.debug('Looking at school %s' % postedJSON['school'])
        school = session.query(School).filter_by(name=postedJSON['school']).first()

        if school is not None:
            if 'distanceToCampus' in postedJSON:
                logger.debug('Distance to Campus %d' % postedJSON['distanceToCampus'])
                allListings = allListings.join(ListingSchool) \
                    .filter(ListingSchool.school_id == school.id,
                            postedJSON['distanceToCampus'] >= ListingSchool.driving_miles)
            else:
                allListings = allListings.join(ListingSchool).filter(ListingSchool.school_id == school.id)
        else:
            logger.error("Could not find school to apply to search filter. postedJSON['school'] : %s" % postedJSON['school'])
    else:
        logger.error("School not found in listing search query")

    logger.debug("School allListings %r" % allListings.all())

    # Pets
    if 'pets' in postedJSON:
        petList = postedJSON['pets']

        if 'dogs' in petList:
            allListings = allListings.filter(Listing.dogs)

        if 'cats' in petList:
            allListings = allListings.filter(Listing.cats)

    # Includes
    if 'includes' in postedJSON:
        includeList = postedJSON['includes']

        if 'furnished' in includeList:
            allListings = allListings.filter(Listing.furnished)

        if 'dishwasher' in includeList:
            allListings = allListings.filter(Listing.dishwasher)

        if 'laundry' in includeList:
            allListings = allListings.filter(Listing.washer, Listing.dryer)

        if 'internet' in includeList:
            allListings = allListings.filter(Listing.internet)

        if 'cable' in includeList:
            allListings = allListings.filter(Listing.cable)

        if 'snowRemoval' in includeList:
            allListings = allListings.filter(Listing.snow_plowing)

        if 'garbageRemoval' in includeList:
            allListings = allListings.filter(Listing.garbage_service)

    # Listing Types
    if 'listingTypes' in postedJSON:
        typeList = postedJSON['listingTypes']

        if 'house' in typeList and 'apartment' in typeList and 'complex' in typeList:
            allListings = allListings.filter(or_(Listing.property_type == 'house',
                                                 Listing.property_type == 'apartment',
                                                 Listing.property_type == 'complex',
                                                 ))
        elif 'house' in typeList and 'apartment' in typeList:
            allListings = allListings.filter(or_(Listing.property_type == 'house',
                                                 Listing.property_type == 'apartment'
                                                 ))
        elif 'house' in typeList and 'complex' in typeList:
            allListings = allListings.filter(or_(Listing.property_type == 'house',
                                                 Listing.property_type == 'complex'
                                                 ))
        elif 'house' in typeList:
            allListings = allListings.filter(Listing.property_type == 'house')

        elif 'apartment' in typeList and 'complex' in typeList:
            allListings = allListings.filter(or_(Listing.property_type == 'apartment',
                                                 Listing.property_type == 'complex'
                                                 ))
        elif 'apartment' in typeList:
            allListings = allListings.filter(Listing.property_type == 'apartment')

        elif 'complex' in typeList:
            allListings = allListings.filter(Listing.property_type == 'complex')
        else:
            logger.error("No Listing Types were defined to search for")

    allListings = allListings.all()

    # sortBy Check
    if 'sortBy' in postedJSON:
        sortedListings = []
        if postedJSON['sortBy'] == 'priceLowToHigh':
            while len(allListings) > 0:
                lowestListing = None
                for listing in allListings:
                    if lowestListing is None:
                        lowestListing = listing
                        continue

                    if listing.price_per_month < lowestListing.price_per_month:
                        lowestListing = listing

                sortedListings.append(lowestListing)
                allListings.remove(lowestListing)

            allListings = sortedListings

        elif postedJSON['sortBy'] == 'priceHighToLow':
            while len(allListings) > 0:
                highestListing = None
                for listing in allListings:
                    if highestListing is None:
                        highestListing = listing
                        continue

                    if listing.price_per_month > highestListing.price_per_month:
                        highestListing = listing

                sortedListings.append(highestListing)
                allListings.remove(highestListing)

            allListings = sortedListings

        elif postedJSON['sortBy'] == 'mostRecent':
            while len(allListings) > 0:
                mostRecentListing = None
                for listing in allListings:
                    if mostRecentListing is None:
                        mostRecentListing = listing
                        continue

                    if listing.date_created < mostRecentListing.date_created:
                        mostRecentListing = listing

                sortedListings.append(mostRecentListing)
                allListings.remove(mostRecentListing)

            allListings = sortedListings

        elif postedJSON['sortBy'] == 'distanceToCampus':
            while len(allListings) > 0:
                closestListing = None
                for listing in allListings:
                    if closestListing is None:
                        closestListing = listing
                        continue

                    if listing.date_created < closestListing.date_created:
                        closestListing = listing

                sortedListings.append(closestListing)
                allListings.remove(closestListing)

            allListings = sortedListings

    listingJSONList = []
    for listing in allListings:
        listingJSONList.append(listing.serialize)

    return jsonify(listings=listingJSONList)
