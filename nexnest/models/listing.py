from datetime import datetime as dt

from nexnest.application import db

from .base import Base

from sqlalchemy import event

from sqlalchemy.orm import relationship


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
    other_pets = db.Column(db.Boolean)
    washer = db.Column(db.Boolean)
    dryer = db.Column(db.Boolean)
    dishwasher = db.Column(db.Boolean)
    air_conditioning = db.Column(db.Boolean)
    handicap = db.Column(db.Boolean)
    furnished = db.Column(db.Boolean)
    utilities_included = db.Column(db.Boolean)
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
    house = relationship("House", backref='listing')

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
            cats,
            dogs,
            other_pets,
            washer,
            dryer,
            dishwasher,
            air_conditioning,
            handicap,
            furnished,
            utilities_included,
            emergency_maintenance,
            snow_plowing,
            garbage_service,
            security_service,
            description,
            num_half_baths,
            num_full_baths,
            time_period,
            apartment_number,
            property_type,
            rent_due):

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
        self.utilities_included = utilities_included
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


def update_date_modified(mapper, connection, target):
    # 'target' is the inserted object
    target.date_modified = dt.now().isoformat()  # Update Date Modified


event.listen(Listing, 'before_update', update_date_modified)
