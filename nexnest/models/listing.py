from datetime import datetime as dt

from nexnest import logger
from nexnest.application import db, app
from nexnest.models.listing_favorite import ListingFavorite

from .base import Base

from sqlalchemy import event

from sqlalchemy.orm import relationship, backref

import os

import googlemaps

from flask_login import current_user


class Listing(Base):
    __tablename__ = 'listings'
    id = db.Column(db.Integer, primary_key=True)
    street = db.Column(db.Text)
    city = db.Column(db.Text)
    state = db.Column(db.String(2))
    zip_code = db.Column(db.String(5))
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    num_bedrooms = db.Column(db.Integer)
    price = db.Column(db.Integer)
    price_per_semester = db.Column(db.Integer)
    price_per_month = db.Column(db.Integer)
    square_footage = db.Column(db.Integer)
    parking = db.Column(db.String)
    cats = db.Column(db.Boolean)
    dogs = db.Column(db.Boolean)
    other_pets = db.Column(db.Text)
    washer = db.Column(db.Boolean)
    dryer = db.Column(db.Boolean)
    dishwasher = db.Column(db.Boolean)
    air_conditioning = db.Column(db.Boolean)
    handicap = db.Column(db.Boolean)
    furnished = db.Column(db.Boolean)
    emergency_maintenance = db.Column(db.Boolean)
    snow_plowing = db.Column(db.Boolean)
    garbage_service = db.Column(db.Boolean)
    security_service = db.Column(db.Boolean)
    description = db.Column(db.Text)
    num_full_baths = db.Column(db.Integer)
    num_half_baths = db.Column(db.Integer)
    apartment_number = db.Column(db.Integer)
    disabled = db.Column(db.Boolean)
    property_type = db.Column(db.Text)
    rent_due = db.Column(db.String(20))
    first_semester_rent_due_date = db.Column(db.Date)
    second_semester_rent_due_date = db.Column(db.Date)
    electricity = db.Column(db.Boolean)
    internet = db.Column(db.Boolean)
    water = db.Column(db.Boolean)
    heat_gas = db.Column(db.Boolean)
    cable = db.Column(db.Boolean)
    washer_free = db.Column(db.Boolean)
    youtube_url = db.Column(db.String(256))
    floor_plan_url = db.Column(db.String(256))
    featured = db.Column(db.Boolean)
    active = db.Column(db.Boolean)
    lat = db.Column(db.Numeric)
    lng = db.Column(db.Numeric)
    banner_photo_url = db.Column(db.Text)

    # monthly_rent_due_date = db.Column(db.Date)

    # school | year | summer
    time_period = db.Column(db.Text)

    time_period_date_range = db.Column(db.Text)

    # This is set to False once a group has been accepted,
    # and completed for the house
    show = db.Column(db.Boolean)

    date_created = db.Column(db.DateTime)
    date_modified = db.Column(db.DateTime)

    groups = relationship("GroupListing", back_populates='listing')
    landlords = relationship("LandlordListing", back_populates='listing')
    tours = relationship("Tour", backref='listing')
    house = relationship("House", backref=backref('listing', uselist=False))
    favorite = relationship("GroupListingFavorite", backref='listing')
    individualFavorite = relationship('ListingFavorite', backref='listing')
    listingTransactionListing = relationship("ListingTransactionListing", backref='listing')
    schools = relationship("ListingSchool", back_populates='listing')
    reports = relationship("ReportListing", backref='listing')

    def __init__(
            self,
            street,
            city,
            state,
            zip_code,
            start_date,
            end_date,
            num_bedrooms,
            price,
            square_footage,
            parking,
            description,
            num_half_baths,
            num_full_baths,
            time_period,
            time_period_date_range,
            property_type,
            rent_due,
            other_pets,
            cats=False,
            dogs=False,
            washer=False,
            dryer=False,
            dishwasher=False,
            air_conditioning=False,
            handicap=False,
            furnished=False,
            emergency_maintenance=False,
            snow_plowing=False,
            garbage_service=False,
            security_service=False,
            electricity=False,
            internet=False,
            water=False,
            heat_gas=False,
            cable=False,
            washer_free=False,
            youtube_url=None,
            apartment_number=None,
            first_semester_rent_due_date=None,
            second_semester_rent_due_date=None,
            featured=False,
            lat=None,
            lng=None,
            banner_photo_url=None,
            show=True,
            active=False):

        self.street = street
        self.city = city
        self.state = state
        self.zip_code = zip_code
        self.start_date = start_date
        self.end_date = end_date
        self.num_bedrooms = num_bedrooms
        self.price = price
        self.square_footage = square_footage
        self.cats = cats
        self.dogs = dogs
        self.other_pets = other_pets
        self.washer = washer
        self.dryer = dryer
        self.dishwasher = dishwasher
        self.air_conditioning = air_conditioning
        self.handicap = handicap
        self.furnished = furnished
        self.emergency_maintenance = emergency_maintenance
        self.snow_plowing = snow_plowing
        self.garbage_service = garbage_service
        self.security_service = security_service
        self.description = description
        self.num_full_baths = num_full_baths
        self.num_half_baths = num_half_baths
        self.apartment_number = apartment_number
        self.disabled = False
        self.active = active  # Landlords have to activate listing
        self.show = show
        self.time_period = time_period
        self.time_period_date_range = time_period_date_range
        self.parking = parking
        self.property_type = property_type
        self.rent_due = rent_due
        self.first_semester_rent_due_date = first_semester_rent_due_date
        self.second_semester_rent_due_date = second_semester_rent_due_date
        self.electricity = electricity
        self.heat_gas = heat_gas
        self.internet = internet
        self.water = water
        self.cable = cable
        self.washer_free = washer_free
        self.youtube_url = youtube_url
        self.featured = featured
        self.banner_photo_url = banner_photo_url

        if self.rent_due == 'monthly':
            self.price_per_month = self.price
            self.price_per_semester = self.price * 6
        elif self.rent_due == 'semester':
            self.price_per_month = self.price / 6
            self.price_per_semester = self.price
        else:
            logger.error('Unknown Rent Due Value while create listing : %s' % self.rent_due)

        # Default Values
        now = dt.now().isoformat()  # Current Time to Insert into Datamodels
        self.date_created = now
        self.date_modified = now

        if lat is None and lng is None:

            gmaps = googlemaps.Client(key=app.config['GOOGLE_MAPS_KEY'])

            geocode = gmaps.geocode(self.address)

            if geocode is not None:
                if len(geocode) > 0:
                    self.lat = geocode[0]['geometry']['location']['lat']
                    self.lng = geocode[0]['geometry']['location']['lng']
        else:
            self.lat = lat
            self.lng = lng

    def __repr__(self):
        return '<Listing %r | %s>' % (self.id, self.street)

    @property
    def shortSerialize(self):
        return {
            'id': self.id,
            'street': self.street,
            'startDate': self.start_date.strftime("%B %d, %Y"),
            'endDate': self.end_date.strftime("%B %d, %Y"),
            'url': '/listing/view/%d' % self.id
        }

    @property
    def serialize(self):
        returnDict = {
            'id': self.id,
            'street': self.street,
            'state': self.state,
            'city': self.city,
            'zipCode': self.zip_code,
            'address': self.address,
            'startDate': self.start_date.strftime("%B %d, %Y"),
            'endDate': self.end_date.strftime("%B %d, %Y"),
            'url': '/listing/view/%d' % self.id,
            'numBedrooms': self.num_bedrooms,
            'price': self.price,
            'pricePerSemester': self.price_per_semester,
            'pricePerMonth': self.price_per_month,
            'squareFootage': self.square_footage,
            'parking': self.parking,
            'cats': self.cats,
            'dogs': self.dogs,
            'washer': self.washer,
            'washerFree': self.washer_free,
            'dryer': self.dryer,
            'dishwasher': self.dishwasher,
            'airConditioning': self.air_conditioning,
            'handicap': self.handicap,
            'furnished': self.furnished,
            'emergencyMaintenance': self.emergency_maintenance,
            'snowPlowing': self.snow_plowing,
            'garbageService': self.garbage_service,
            'securityService': self.security_service,
            'description': self.description,
            'numFullBaths': self.num_full_baths,
            'numHalfBaths': self.num_half_baths,
            'apartmentNumber': self.apartment_number,
            'propertyType': self.property_type,
            'electricity': self.electricity,
            'internet': self.internet,
            'water': self.water,
            'heatGas': self.heat_gas,
            'cable': self.cable,
            'featured': self.featured,
            'timePeriod': self.time_period,
            'timePeriodDateRange': self.time_period_date_range,
            'priceTerm': self.rent_due,
            'bannerPhotoURL': self.getBannerPhotoURL(),
            'lat': float(self.lat),
            'long': float(self.lng)
        }

        # if current_user is not None:
        #     if current_user.is_authenticated:
        #         if self.isFavoritedBy(current_user):
        #             returnDict['isFavorited'] = True

        # returnDict['isFavorited'] = False

        return returnDict

    @property
    def briefStreet(self):
        return self.street[:22] + '...'

    @property
    def pricePerMonth(self):
        if self.rent_due == 'montly':
            return self.price
        else:
            return self.price / 6

    @property
    def hasAcceptedGroupListing(self):
        for groupListing in self.groups:
            if groupListing.accepted:
                return True

        return False

    @property
    def hasUtilities(self):
        return self.electricity or self.water or self.heat_gas or self.internet or self.cable

    @property
    def hasServices(self):
        return self.handicap or self.snow_plowing or self.emergency_maintenance or self.security_service or self.garbage_service

    @property
    def hasAppliances(self):
        return self.washer or self.dryer or self.air_conditioning or self.dishwasher

    @property
    def hasPets(self):
        return self.dogs or self.cats or (len(self.other_pets) > 0)

    @property
    def hasTours(self):
        if not self.hasHouse() and not self.hasAcceptedGroupListing:
            if len(self.tours) > 0:
                return True

        return False

    @property
    def address(self):
        return '%s, %s %s, %s' % (self.street, self.city, self.state, self.zip_code)

    @property
    def hasAcceptedHouseRequest(self):
        return self.hasAcceptedGroupListing

    @property
    def briefAddress(self):
        return self.address[:22] + "..."

    def isEditableBy(self, user):
        if self.hasHouse() or self.hasAcceptedGroupListing:
            return False

        if user in self.landLordsAsUsers():
            return True

        return False

    def isViewableBy(self, user):
        if self.isEditableBy(user):
            return True
        elif self.active and self.show:
            return True

        return False

    def isFavoritedBy(self, user):
        return ListingFavorite.query.filter_by(listing=self, user=user).count() == 1

    def landLords(self):
        landlords = []

        for landlordListing in self.landlords:
            landlords.append(landlordListing.landlord)

        return landlords

    def landLordsAsUsers(self):
        landlords = []

        for landlordListing in self.landlords:
            landlords.append(landlordListing.landlord.user)

        return landlords

    def isLandlord(self, current_user):
        return current_user in self.landLordsAsUsers

    def getPhotoURLs(self):
        photoURLs = []
        folderPath = os.path.join(app.config['UPLOAD_FOLDER'], 'listings', str(self.id), 'pictures')

        if os.path.exists(folderPath):
            for filename in os.listdir(folderPath):
                photoURLs.append("/uploads/listings/%r/pictures/%s" % (self.id, filename.replace("\'", "")))
        return photoURLs

    def getBannerPhotoURL(self):
        if self.banner_photo_url is not None:
            return self.banner_photo_url
        else:
            photoURL = []
            folderPath = os.path.join(app.config['UPLOAD_FOLDER'], 'listings', str(self.id), 'bannerPhoto')

            if os.path.exists(folderPath):
                for filename in os.listdir(folderPath):
                    photoURL.append("/uploads/listings/%r/bannerPhoto/%s" % (self.id, filename.replace("\'", "")))

            if len(photoURL) > 0:
                return photoURL[0]
            else:
                return None

    def hasHouse(self):
        return len(self.house) > 0

    def isForSchool(self, school):
        for listingSchool in self.schools:
            if listingSchool.school == school:
                return True

        return False


def update_date_modified(mapper, connection, target):  # pylint: disable=unused-argument
    # 'target' is the inserted object
    target.date_modified = dt.now().isoformat()  # Update Date Modified


event.listen(Listing, 'before_update', update_date_modified)
