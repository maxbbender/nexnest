from datetime import datetime as dt

from nexnest.application import db, app

from .base import Base

from sqlalchemy import event

from sqlalchemy.orm import relationship, backref

import os


# class PostReport(Base):
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
    time_period = db.Column(db.Text)
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

    # monthly_rent_due_date = db.Column(db.Date)

    # This is for whether or not the landlord has deleted
    # the listing. This comes into play for checking dates
    # when a landlord creates a new listing at the same
    # address
    active = db.Column(db.Boolean)

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
            second_semester_rent_due_date=None):

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
        self.active = False  # Landlords have to activate listing
        self.show = False  # Landlord have to activate listing
        self.time_period = time_period
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

        # Default Values
        now = dt.now().isoformat()  # Current Time to Insert into Datamodels
        self.date_created = now
        self.date_modified = now

    def __repr__(self):
        return '<Listing %r>' % self.id

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

    def getPhotoURLs(self):
        photoURLs = []
        folderPath = os.path.join(app.config['UPLOAD_FOLDER'], 'listings', str(self.id))

        if os.path.exists(folderPath):

            for filename in os.listdir(folderPath):
                photoURLs.append("/uploads/listings/%r/%s" % (self.id, filename.replace("\'", "")))
        return photoURLs



    def hasHouse(self):
        return len(self.house) > 0


def update_date_modified(mapper, connection, target):  # pylint: disable=unused-argument
    # 'target' is the inserted object
    target.date_modified = dt.now().isoformat()  # Update Date Modified


event.listen(Listing, 'before_update', update_date_modified)
