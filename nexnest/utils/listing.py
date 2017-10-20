import os

from flask import current_app as app
from flask import flash

from nexnest import db
from nexnest.utils.misc import idGenerator

from nexnest.utils.file import allowed_file


def updateListing(listing, form):
    listing.street = form.street.data
    listing.city = form.city.data
    listing.state = form.state.data
    listing.zip_code = form.zip_code.data
    listing.start_date = form.start_date.data
    listing.end_date = form.end_date.data
    listing.time_period = form.time_period.data
    listing.apartment_number = form.apartment_number.data
    listing.num_bedrooms = form.num_bedrooms.data
    listing.num_full_baths = form.num_full_baths.data
    listing.num_half_baths = form.num_half_baths.data
    listing.price = form.price.data
    listing.square_footage = form.square_footage.data
    listing.parking = form.parking.data
    listing.cats = form.cats.data
    listing.dogs = form.dogs.data
    listing.other_pets = form.other_pets.data
    listing.washer = form.washer.data
    listing.dryer = form.dryer.data
    listing.dishwasher = form.dishwasher.data
    listing.air_conditioning = form.air_conditioning.data
    listing.handicap = form.handicap.data
    listing.furnished = form.furnished.data
    listing.emergency_maintenance = form.emergency_maintenance.data
    listing.snow_plowing = form.snow_plowing.data
    listing.garbage_service = form.garbage_service.data
    listing.security_service = form.security_service.data
    listing.description = form.description.data
    listing.rent_due = form.rent_due.data
    listing.property_type = form.property_type.data
    listing.electricity = form.electricity.data
    listing.internet = form.internet.data
    listing.water = form.water.data
    listing.heat_gas = form.heat_gas.data
    listing.cable = form.cable.data
    listing.washer_free = form.washer_free.data
    listing.youtube_url = form.youtube_url.data
    listing.time_period_date_range = form.time_period_date_range.data

    if form.property_type == 'apartment':
        listing.apartment_number = form.apartment_number.data

    if form.rent_due == 'semester':
        listing.first_semester_rent_due_date = form.first_semester_rent_due_date.data
        listing.second_semester_rent_due_date = form.second_semester_rent_due_date.data

    return listing


def updatePictures(listing, request):
    # Make sure to delete the original banner photo in case of different extension
    bannerPhotos = os.listdir(listing.bannerPath)
    if len(bannerPhotos) > 0:
        for photo in bannerPhotos:
            fullFilePath = os.path.join(listing.bannerPath, photo)
            try:
                os.remove(fullFilePath)
            except OSError as err:
                app.logger.warning('Tried to delete file %s and got error %s' % (fullFilePath, err))

    # Lets add the photos
    uploadedFiles = request.files.getlist("bannerPicture")
    for file in uploadedFiles:
        if file.filename == '':
            continue

        if file and allowed_file(file.filename):
            extension = os.path.splitext(file.filename)[1]
            filename = "listing" + str(listing.id) + "banner" + idGenerator() + extension
            savePath = os.path.join(listing.bannerPath, filename)

            while os.path.exists(savePath):
                filename = "listing" + str(listing.id) + "banner" + idGenerator() + extension
                savePath = os.path.join(listing.bannerPath, filename)

            file.save(savePath)
            listing.banner_photo_url = '/uploads/listings/%s/bannerPhoto/%s' % (listing.id, filename)
            db.session.commit()
        else:
            flash("Error saving file %s" % file.filename, 'danger')

    flash('Listing Updated', 'info')
