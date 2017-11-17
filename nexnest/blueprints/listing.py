import datetime
import json
import os
import re
from pprint import pprint
from shutil import copy2

from flask import current_app as app
from flask import (Blueprint, flash, jsonify, redirect, render_template,
                   request, url_for)
from flask_login import current_user, login_required
from nexnest import csrf, db
from nexnest.forms import (GroupListingForm, ListingForm, ListingReportForm,
                           PhotoForm, SuggestListingForm, TourForm, CreateGroupForm)
from nexnest.models.landlord_listing import LandlordListing
from nexnest.models.listing import Listing
from nexnest.models.listing_school import ListingSchool
from nexnest.models.school import School
from nexnest.utils.file import allowed_file, isPDF
from nexnest.utils.flash import flash_errors
from nexnest.utils.misc import idGenerator
from nexnest.utils.school import allSchoolsAsStrings
from sqlalchemy import or_
from sqlalchemy.sql.expression import func
from werkzeug import secure_filename  # pylint: disable=E0611

from nexnest.utils.listing import updateListing, updatePictures
from nexnest.decorators import listing_viewable, listing_editable

listings = Blueprint('listings', __name__, template_folder='../templates')

session = db.session


@listings.route('/listing/view/<int:listingID>', methods=['GET', 'POST'])
@listing_viewable
def viewListing(listingID):
    listing = Listing.query.filter_by(id=listingID).first_or_404()
    if current_user.is_authenticated:
        myGroups = current_user.accepted_groups
    else:
        myGroups = None
    return render_template('detailedListing.html',
                           suggestListingForm=SuggestListingForm(),
                           requestTourForm=TourForm(),
                           requestListingForm=GroupListingForm(),
                           listing=listing,
                           groups=myGroups,
                           title='Listing',
                           pictures=listing.getPhotoURLs(),
                           bannerPhoto=listing.banner_photo_url,
                           ListingReportForm=ListingReportForm(),
                           createGroupForm=CreateGroupForm())


@listings.route('/listing/create', methods=['GET', 'POST'])
@login_required
def createListing():
    app.logger.debug('/listing/create createListing()')
    # User can only create listing if landlord
    if current_user.isLandlord or current_user.isAdmin:
        form = ListingForm(request.form)

        if form.validate_on_submit():
            app.logger.debug('POST form : %r' % form)
            app.logger.debug('TimePeriodDateRange : %s' % form.time_period_date_range.data)
            app.logger.debug('Start Date : %r' % form.start_date.data)

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

            if newListing.property_type == 'apartment':
                newListing.apartment_number = form.apartment_number.data

            app.logger.debug('newListing.property_type : %r' % newListing.property_type)
            app.logger.debug('newListing.street : %r' % newListing.street)
            app.logger.debug('newListing.city : %r' % newListing.city)
            app.logger.debug('newListing.zip_code : %r' % newListing.zip_code)
            app.logger.debug('newListing.apartment_number : %r' % newListing.apartment_number)

            otherListingsWithSameAddress = None
            if newListing.property_type == 'apartment':
                otherListingsWithSameAddress = session.query(Listing) \
                    .filter_by(street=newListing.street,
                               city=newListing.city,
                               state=newListing.state,
                               zip_code=newListing.zip_code,
                               apartment_number=newListing.apartment_number,
                               active=True
                               ) \
                    .all()
            else:
                otherListingsWithSameAddress = session.query(Listing) \
                    .filter_by(street=newListing.street,
                               city=newListing.city,
                               state=newListing.state,
                               zip_code=newListing.zip_code,
                               active=True
                               ) \
                    .all()

            app.logger.debug('Found other listings with the same address : %r' % otherListingsWithSameAddress)

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

                newListing.createUploadDirectories()

                # Now we need to figure out whether this is an Admin creating the listing
                # or if it is a landlord.

                # Lets assign the current user to be the landlord of this listing
                newLandLordListing = LandlordListing(landlord=current_user.landlord[0],
                                                     listing=newListing)
                session.add(newLandLordListing)
                session.commit()

                # Now we want to define the colleges this listing is associated with
                collegeNames = json.loads(form.colleges.data)

                for collegeName in collegeNames:
                    school = session.query(School).filter_by(name=collegeName).first()

                    if school is not None:
                        newListingSchool = ListingSchool(listing=newListing, school=school)
                        session.add(newListingSchool)
                        session.commit()
                        app.logger.debug('newListingSchool %r' % newListingSchool)
                    else:
                        app.logger.error('Could not find school with name %s. Could not associated listing %r with school' % (collegeName, newListing))

                app.logger.debug('form.colleges.data : %s' % form.colleges.data)
                app.logger.debug('collegeNames %r' % collegeNames)

                if newListing.property_type == 'apartment':
                    newListing.apartment_number = form.apartment_number.data

                if newListing.rent_due == 'semester':
                    newListing.first_semester_rent_due_date = form.first_semester_rent_due_date.data
                    newListing.second_semester_rent_due_date = form.second_semester_rent_due_date.data

                session.commit()

                if 'floor_plan' in request.files:
                    file = request.files['floor_plan']

                    if file and isPDF(file.filename):
                        filename = secure_filename(request.files['floor_plan'].filename)

                        if file and allowed_file(filename):
                            file.save(os.path.join(newListing.uploadPath, 'floorplan.pdf'))

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
        flash("Only Landlords can create listings", 'warning')
        return redirect(url_for('indexs.index'))


@listings.route('/listing/clone/<listingID>', methods=['GET', 'POST'])
@login_required
@listing_editable
def cloneListing(listingID):
    listingToClone = Listing.query.filter_by(id=listingID).first_or_404()

    if listingToClone.isCloneableBy(current_user):
        # Get colleges associated with the listing
        selectedSchools = ListingSchool.query.filter_by(listing=listingToClone).all()

        # Get the previous pictures
        folderPath = os.path.join(app.config['UPLOAD_FOLDER'], 'listings', str(listingID))
        listingPicturePath = os.path.join(folderPath, 'pictures')
        picturePaths = os.listdir(listingPicturePath)

        # If it is an apartment we need to pass the apartment number along as well
        # Because if it is an apartment we need to take the apt number and end date in account
        # When determining if the listing is cloneable
        aptNumber = None
        if listingToClone.property_type == 'apartment':
            aptNumber = listingToClone.apartment_number

        form = ListingForm(obj=listingToClone)
        return render_template('/landlord/createListing.html',
                               form=form,
                               title='Create Listing',
                               schools=allSchoolsAsStrings(),
                               selectedSchools=selectedSchools,
                               picturePaths=picturePaths,
                               startDate=listingToClone.start_date,
                               endDate=listingToClone.end_date,
                               aptNumber=aptNumber)
    else:
        flash("You are not the landlord of this listing", 'warning')

    return redirect(url_for('listings.viewListing',
                            listingID=listingID))


@listings.route('/listing/edit/<listingID>', methods=['GET', 'POST'])
@login_required
@listing_editable
def editListing(listingID):
    listing = Listing.query.filter_by(id=listingID).first_or_404()

    # Get colleges associated with the listing
    selectedSchools = ListingSchool.query.filter_by(listing=listing).all()

    # Listing Folder Path
    folderPath = os.path.join(app.config['UPLOAD_FOLDER'], 'listings', str(listingID))

    # Get the pictures from the liting
    listingPicturePath = os.path.join(folderPath, 'pictures')
    if os.path.exists(listingPicturePath):
        picturePaths = os.listdir(listingPicturePath)
    else:
        picturePaths = None

    form = ListingForm(obj=listing)

    form.start_date.data = listing.start_date.strftime('%Y-%m-%d')
    form.end_date.data = listing.end_date.strftime('%Y-%m-%d')

    if form.validate_on_submit():
        listing = updateListing(listing, form)
        updatePictures(listing, request)

        session.commit()

        if listing.active:
            flash('Listing has been updated', 'success')
            return redirect(url_for('listings.viewListing',
                                    listingID=listingID))
        else:
            return redirect(url_for('landlords.landlordDashboard') + '#checkoutTab')

    else:
        flash_errors(form)
        return render_template('/landlord/editListing.html',
                               form=form,
                               title='Edit Listing',
                               listingID=listingID,
                               schools=allSchoolsAsStrings(),
                               selectedSchools=selectedSchools,
                               picturePaths=picturePaths,
                               startDate=listing.start_date,
                               endDate=listing.end_date,
                               bannerPath=listing.banner_photo_url)


@listings.route('/listing/delete/<listingID>', methods=['GET'])
@login_required
@listing_editable
def deleteListing(listingID):
    listing = Listing.query.filter_by(id=listingID).first()

    if listing is not None:
        db.session.delete(listing)
        db.session.commit()
        flash('Listing Deleted!', 'success')
    else:
        flash('Unable to find that listing to delete', 'warning')
        app.logger.warning('Listing was attempted to delete but does not exists %d' % listingID)

    return redirect(url_for('landlords.landlordDashboard'))


@listings.route("/listing/upload/<listingID>", methods=["POST"])
@login_required
@listing_editable
@csrf.exempt
def upload(listingID):
    """Handle the upload of a file."""

    # Is the upload using Ajax, or a direct POST by the form?
    is_ajax = True

    listing = Listing.query.filter_by(id=listingID).first_or_404()

    # Can this listing be changed by the current user
    if listing.isEditableBy(current_user):
        try:
            listingUploadFolder = os.path.join(app.config['UPLOAD_FOLDER'], 'listings', str(listing.id))
            if not os.path.exists(listingUploadFolder):
                os.makedirs(listingUploadFolder)

            listingPictureFolder = os.path.join(listingUploadFolder, 'pictures')
            if not os.path.exists(listingPictureFolder):
                os.makedirs(listingPictureFolder)
        except:
            app.logger.error('Could not create directories')

    # Now we uplopad the files
    for file in request.files.getlist("pictures"):
        if file and allowed_file(file.filename):
            extension = os.path.splitext(file.filename)[1]

            filename = "listing" + listingID + "photo" + idGenerator() + extension

            savePath = os.path.join(listingPictureFolder, filename)

            while os.path.exists(savePath):
                filename = "listing" + listingID + "photo" + idGenerator() + extension
                savePath = os.path.join(listingPictureFolder, filename)

            file.save(savePath)
            app.logger.debug("filename is " + filename)
            app.logger.debug("file saved at %s" % savePath)

    if is_ajax:
        return jsonify(results={'success': True})
    else:
        return redirect(url_for("listings.view", listingID=listing.id))


@listings.route("/listing/delete/<listingID>/<filename>", methods=["POST"])
@login_required
@listing_editable
def deletePhoto(listingID, filename):
    listing = Listing.query.filter_by(id=listingID).first_or_404()

    if listing.isEditableBy(current_user):

        folderPath = os.path.join(app.config['UPLOAD_FOLDER'], 'listings', str(listingID))
        listingPicturePath = os.path.join(folderPath, 'pictures')
        os.remove(listingPicturePath + "/" + filename)

        return jsonify(results={'success': True})
    else:
        return jsonify(results={'success': False, 'message': 'Permissions Error'})


@listings.route("/listing/deleteBanner/<listingID>/<filename>", methods=["POST"])
@login_required
@listing_editable
def deleteBannerPhoto(listingID, filename):
    listing = Listing.query.filter_by(id=listingID).first_or_404()

    if listing.isEditableBy(current_user):
        folderPath = os.path.join(app.config['UPLOAD_FOLDER'], 'listings', str(listingID))
        listingPicturePath = os.path.join(folderPath, 'bannerPhoto')
        os.remove(listingPicturePath + "/" + filename)
        return jsonify(results={'success': True})
    else:
        return jsonify(results={'success': False, 'message': 'Permissions Error'})


# THIS ONE IS FOR BANNER PHOTOS!
@listings.route('/listing/<listingID>/uploadPhotos', methods=['GET', 'POST'])
@login_required
@listing_editable
def uploadPhotos(listingID):
    listing = Listing.query.filter_by(id=listingID).first_or_404()
    bannerPath = None
    picturePaths = None
    form = PhotoForm()

    if form.validate_on_submit():
        uploadedFiles = request.files.getlist("bannerPicture")
        for file in uploadedFiles:
            if file.filename == '':
                continue

            if file and allowed_file(file.filename):
                extension = os.path.splitext(file.filename)[1]
                filename = "listing" + listingID + "banner" + idGenerator() + extension
                savePath = os.path.join(listing.bannerPath, filename)

                while os.path.exists(savePath):
                    filename = "listing" + listingID + "banner" + idGenerator() + extension
                    savePath = os.path.join(listing.bannerPath, filename)

                file.save(savePath)

                listing.banner_photo_url = '/uploads/listings/%s/bannerPhoto/%s' % (listingID, filename)
                session.commit()
            else:
                flash("Error saving file %s" % file.filename, 'danger')

        if form.nextAction.data == 'checkout':
            flash('Listing Created!', 'success')
            return redirect(url_for('landlords.landlordDashboard'))
        elif form.nextAction.data == 'createNew':
            flash('Listing Created!', 'success')
            return redirect(url_for('listings.createListing'))
        elif form.nextAction.data == 'createCopy':
            flash('Listing Created!', 'success')
            return redirect(url_for('listings.cloneListing', listingID=listingID))
            # selectedSchools = ListingSchool.query.filter_by(listing_id=listingID).all()
            # # Get Pictures
            # form = ListingForm()
            # return render_template('/landlord/createListing.html',
            #                        form=form,
            #                        title='Create Listing',
            #                        schools=allSchoolsAsStrings(),
            #                        selectedSchools=selectedSchools)
        else:
            app.logger.debug('Unknown nextAction : %s' % form.nextAction.data)
    else:
        # Does the current listing have any listing photos?
        app.logger.debug("Trying to copy photos from one listing to another")

        # Is there any pictures for the listing
        # if not lets try to find another listing with the same address and copy it's pictures
        picturePaths = listing.allPictureURL
        if picturePaths is not None and len(picturePaths) == 0:

            # Are there other listings with the same address?
            otherListing = Listing.query.filter_by(city=listing.city,
                                                   state=listing.state,
                                                   street=listing.street,
                                                   zip_code=listing.zip_code) \
                .first()

            app.logger.debug("Found listing with same address %r" % otherListing)

            if otherListing is not None:
                # Let's get the photos from that listing and copy them over....
                otherListingPictureFolder = os.path.join(app.config['UPLOAD_FOLDER'], 'listings', str(otherListing.id), 'pictures')
                otherListingPicturePaths = os.listdir(otherListingPictureFolder)

                app.logger.debug('Other Listing otherListingPicturePaths : %r' % otherListingPicturePaths)

                for picture in otherListingPicturePaths:
                    copy2(os.path.join(otherListingPictureFolder, picture), listing.picturePath)

            app.logger.debug("Copied photos!")
            app.logger.debug("NewListing picturePaths %r" % picturePaths)

        # Get the bannerPhoto from the listing
        bannerlistingPicturePath = listing.bannerPath
        if os.path.exists(bannerlistingPicturePath):
            bannerPathList = os.listdir(bannerlistingPicturePath)

            if len(bannerPathList) > 0:
                bannerPath = bannerPathList[0]
                app.logger.debug("Found Banner Photos %r" % bannerPath)
            else:
                # Let's see if there are other listings w/ same address
                otherListing = Listing.query.filter_by(city=listing.city,
                                                       state=listing.state,
                                                       street=listing.street,
                                                       zip_code=listing.zip_code) \
                    .first()

                app.logger.debug("Found listing with same address %r" % otherListing)

                if otherListing is not None:
                    otherListingBannerFolder = os.path.join(app.config['UPLOAD_FOLDER'], 'listings', str(otherListing.id), 'bannerPhoto')
                    otherListingBannerPaths = os.listdir(otherListingBannerFolder)

                    app.logger.debug('Other Listing otherListingBannerPaths : %r' % otherListingBannerPaths)

                    for picture in otherListingBannerPaths:
                        copy2(os.path.join(otherListingBannerFolder, picture), bannerlistingPicturePath)

                    app.logger.debug('Copied Photos!')

                bannerPathList = os.listdir(bannerlistingPicturePath)
                if len(bannerPathList) > 0:
                    bannerPath = bannerPathList[0]
                    listing.banner_photo_url = '/uploads/listings/%s/bannerPhoto/%s' % (listing.id, bannerPath)
                    session.commit()
                    app.logger.debug("NewListing bannerPath %r" % bannerPath)

        else:
            bannerPath = None

        return render_template('/landlord/uploadPhotos.html',
                               form=form,
                               title='Upload Photos',
                               listingID=listingID,
                               picturePaths=picturePaths,
                               bannerPath=listing.banner_photo_url)


@listings.route('/listing/search/AJAX', methods=['POST', 'GET'])
def searchListingsAJAX():
    app.logger.debug("@listings.route('/listing/search/AJAX")
    postedJSON = request.get_json(force=True)
    app.logger.debug("Incoming POSTEDJSON")
    app.logger.debug(pprint(postedJSON))

    # Required Fields : `bedrooms` | `minPrice` | `maxPrice` | `priceTerm` | `school`
    allListings = session.query(Listing).filter(Listing.active == True,
                                                Listing.show == True)

    # featuredListings = Listings.query.filter(Listing.active == True,
    #                                          Listing.featured == True)

    # Bedroom Checks:
    if 'bedrooms' in postedJSON:
        if postedJSON['bedrooms'] < 4:
            allListings = allListings.filter(Listing.num_bedrooms == postedJSON['bedrooms'])
        else:
            allListings = allListings.filter(Listing.num_bedrooms >= 4)
    else:
        app.logger.error("Bedrooms not found in listing search query")

    app.logger.debug("Bedrooms allListings %r" % allListings.all())

    # Price Checks
    if 'minPrice' in postedJSON and 'maxPrice' in postedJSON:
        allListings = allListings.filter(Listing.price_per_month >= postedJSON['minPrice'], Listing.price_per_month <= postedJSON['maxPrice'])
    else:
        app.logger.error('Minimum or Maximum price not found in listing search query')

    app.logger.debug("Price allListings %r" % allListings.all())

    # Term Checks
    if 'term' in postedJSON:
        # schoolYearPattern = re.compile(r"(Fall '\d{2}- Spring '\d{2})")
        schoolYearPattern = re.compile(r"(\d{4}-\d{4})")
        match = schoolYearPattern.match(postedJSON['term'])
        if match:
            app.logger.debug("Term School | Year : %s" % match.group(1))
            allListings = allListings.filter(Listing.time_period_date_range == match.group(1),
                                             or_(Listing.time_period == 'school',
                                                 Listing.time_period == 'year'))
        else:
            summerPattern = re.compile(r"(\d{4})")
            match = summerPattern.match(postedJSON['term'])

            if match:
                app.logger.debug("Term Summer")
                allListings = allListings.filter(Listing.time_period_date_range == match.group(1),
                                                 Listing.time_period == 'summer')
            else:
                app.logger.error("term input is invalid and does not match any patterns defined. postedJSON['term'] : %s" % postedJSON['term'])
    else:
        app.logger.error("Term not found in listing search query")

    app.logger.debug("Term allListings %r" % allListings.all())

    # School
    if 'school' in postedJSON:
        app.logger.debug('Looking at school %s' % postedJSON['school'])
        school = session.query(School).filter_by(name=postedJSON['school']).first()

        if school is not None:
            if 'distanceToCampus' in postedJSON:
                app.logger.debug('Distance to Campus %d' % postedJSON['distanceToCampus'])
                allListings = allListings.join(ListingSchool) \
                    .filter(ListingSchool.school_id == school.id,
                            postedJSON['distanceToCampus'] >= ListingSchool.driving_miles)
            else:
                allListings = allListings.join(ListingSchool).filter(ListingSchool.school_id == school.id)
        else:
            app.logger.error("Could not find school to apply to search filter. postedJSON['school'] : %s" % postedJSON['school'])
    else:
        app.logger.error("School not found in listing search query")

    app.logger.debug("School allListings %r" % allListings.all())

    # Pets
    if 'pets' in postedJSON:
        petList = postedJSON['pets']

        if 'dogs' in petList:
            allListings = allListings.filter(Listing.dogs)

        if 'cats' in petList:
            allListings = allListings.filter(Listing.cats)

    app.logger.debug("Pets allListings %r" % allListings.all())

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

    app.logger.debug("Includes allListings %r" % allListings.all())

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
            app.logger.error("No Listing Types were defined to search for")

    standardListings = allListings.filter(Listing.featured == False).all()
    featuredListings = allListings.filter(Listing.featured == True).order_by(func.random()).limit(2).all()

    unAddedFeaturedListings = allListings.filter(Listing.featured == True).all()

    for listing in unAddedFeaturedListings:
        if listing not in featuredListings:
            standardListings.append(listing)

    app.logger.debug("Standard allListings %r" % standardListings)
    app.logger.debug("Featured allListings %r" % featuredListings)

    # sortBy Check
    if 'sortBy' in postedJSON:
        sortedListings = []
        if postedJSON['sortBy'] == 'priceLowToHigh':
            while len(standardListings) > 0:
                lowestListing = None
                for listing in standardListings:
                    if lowestListing is None:
                        lowestListing = listing
                        continue

                    if listing.price_per_month < lowestListing.price_per_month:
                        lowestListing = listing

                sortedListings.append(lowestListing)
                standardListings.remove(lowestListing)

            standardListings = sortedListings

        elif postedJSON['sortBy'] == 'priceHighToLow':
            while len(standardListings) > 0:
                highestListing = None
                for listing in standardListings:
                    if highestListing is None:
                        highestListing = listing
                        continue

                    if listing.price_per_month > highestListing.price_per_month:
                        highestListing = listing

                sortedListings.append(highestListing)
                standardListings.remove(highestListing)

            standardListings = sortedListings

        elif postedJSON['sortBy'] == 'mostRecent':
            while len(standardListings) > 0:
                mostRecentListing = None
                for listing in standardListings:
                    if mostRecentListing is None:
                        mostRecentListing = listing
                        continue

                    if listing.date_created < mostRecentListing.date_created:
                        mostRecentListing = listing

                sortedListings.append(mostRecentListing)
                standardListings.remove(mostRecentListing)

            standardListings = sortedListings

        elif postedJSON['sortBy'] == 'distanceToCampus':
            while len(standardListings) > 0:
                closestListing = None
                for listing in standardListings:
                    if closestListing is None:
                        closestListing = listing
                        continue

                    if listing.date_created < closestListing.date_created:
                        closestListing = listing

                sortedListings.append(closestListing)
                standardListings.remove(closestListing)

            standardListings = sortedListings

    listingJSONList = []
    for listing in standardListings:
        listingDict = listing.serialize

        if current_user.is_authenticated:
            listingDict['isFavorited'] = listing.isFavoritedBy(current_user)
        else:
            listingDict['isFavorited'] = False

        listingSchool = ListingSchool.query.filter_by(listing=listing, school=school).first()

        if listingSchool is not None:
            if listingSchool.driving_time is not None:
                listingDict['drivingTime'] = float(listingSchool.driving_time)

            if listingSchool.driving_miles is not None:
                listingDict['drivingMiles'] = float(listingSchool.driving_miles)

            if listingSchool.walking_time is not None:
                listingDict['walkingTime'] = float(listingSchool.walking_time)

            if listingSchool.walking_miles is not None:
                listingDict['walkingMiles'] = float(listingSchool.walking_miles)

        listingJSONList.append(listingDict)

    # app.logger.debug("Standard Listings")
    # for tempDict in listingJSONList:
    #     pprint(tempDict)

    featuredJSONList = []
    for listing in featuredListings:
        listingDict = listing.serialize

        if current_user.is_authenticated:
            listingDict['isFavorited'] = listing.isFavoritedBy(current_user)
        else:
            listingDict['isFavorited'] = False

        listingSchool = ListingSchool.query.filter_by(listing=listing, school=school).first()

        if listingSchool is not None:
            if listingSchool.driving_time is not None:
                listingDict['drivingTime'] = float(listingSchool.driving_time)

            if listingSchool.driving_miles is not None:
                listingDict['drivingMiles'] = float(listingSchool.driving_miles)

            if listingSchool.walking_time is not None:
                listingDict['walkingTime'] = float(listingSchool.walking_time)

            if listingSchool.walking_miles is not None:
                listingDict['walkingMiles'] = float(listingSchool.walking_miles)

        featuredJSONList.append(listingDict)

    school = School.query.filter_by(name=postedJSON['school']).first()

    returnDict = {'listings': listingJSONList,
                  'featuredListings': featuredJSONList}

    if school is not None:
        returnDict['school'] = school.serialize
    else:
        returnDict['school'] = None

    if current_user.is_authenticated:
        if not current_user.isLandlord:
            returnDict['currentUserSchool'] = current_user.school.serialize
        else:
            returnDict['currentUserSchool'] = None
    else:
        returnDict['currentUserSchool'] = None

    return jsonify(returnDict)


@listings.route('/listings/getAddresses/<schoolName>')
# @login_required
def getListingAddresses(schoolName=None):
    schoolToSearch = None
    # if schoolName is None:
    #     if current_user.school is not None:
    #         schoolToSearch = current_user.school
    # else:
    schoolToSearch = School.query.filter_by(name=schoolName).first_or_404()

    # app.logger.debug("Looking for listings that have school %r" % current_user.school)
    listings = Listing.query. \
        join(Listing.schools). \
        filter(ListingSchool.school_id == schoolToSearch.id). \
        filter(Listing.active == True). \
        all()

    app.logger.debug('listings %r' % listings)

    returnListingList = []

    for listing in listings:
        serialiedListing = listing.serialize
        returnListingList.append({'value': serialiedListing['address'], 'id': listing.id})

    return jsonify({'listings': returnListingList})
