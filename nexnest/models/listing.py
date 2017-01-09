from datetime import datetime as dt

from nexnest.application import db

from .base import Base

from sqlalchemy import event


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
    unit_type = db.Column(db.String(10))
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

    def __init__(
            self,
            street,
            city,
            state,
            zip_code,
            start_date,
            end_date,
            unit_type,
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
            num_full_baths):

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

        self.active = True
        self.show = True

        valid_parking_types = ['onstreet', 'offstreet', 'none']
        valid_unit_types = ['room', 'house', 'complex', 'apartment']

        if unit_type in valid_unit_types:
            self.unit_type = unit_type
        else:
            self.unit_type = 'apartment'

        if parking in valid_parking_types:
            self.parking = parking
        else:
            self.parking = 'none'

        # Default Values
        now = dt.now().isoformat()  # Current Time to Insert into Datamodels
        self.date_created = now
        self.date_modified = now

    def __repr__(self):
        return '<Listing %r>' % self.id


def update_date_modified(mapper, connection, target):
    # 'target' is the inserted object
    target.date_modified = dt.now().isoformat()  # Update Date Modified


event.listen(Listing, 'before_update', update_date_modified)
