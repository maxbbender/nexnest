from datetime import datetime as dt

from sqlalchemy import event
from sqlalchemy.orm import relationship

from nexnest import db
from flask import current_app as app


from .base import Base
import googlemaps


class School(Base):
    __tablename__ = 'schools'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    street = db.Column(db.Text)
    city = db.Column(db.Text)
    state = db.Column(db.String(2))
    zip_code = db.Column(db.String(5))
    phone = db.Column(db.String(10))
    website = db.Column(db.Text)
    lat = db.Column(db.Numeric)
    lng = db.Column(db.Numeric)
    date_created = db.Column(db.DateTime)
    date_modified = db.Column(db.DateTime)
    users = relationship("User", backref='school')
    listings = relationship("ListingSchool", back_populates='school')

    def __init__(self,
                 name,
                 street=None,
                 city=None,
                 state=None,
                 zip_code=None,
                 phone=None,
                 website=None,
                 lat=None,
                 lng=None):

        self.name = name
        self.street = street
        self.city = city
        self.state = state
        self.zip_code = zip_code
        self.phone = phone
        self.website = website

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

        # Default Values
        now = dt.now().isoformat()  # Current Time to Insert into Datamodels
        self.date_created = now
        self.date_modified = now

    def __repr__(self):
        return '<School %r>' % self.name

    @property
    def serialize(self):
        returnDict = {
            'name': self.name,
            'street': self.street,
            'city': self.city,
            'state': self.state,
            'zipCode': self.zip_code,
            'phone': self.phone,
            'website': self.website,
            'address': self.address
        }
        if self.lat is not None and self.lng is not None:
            returnDict['lat'] = float(self.lat)
            returnDict['lng'] = float(self.lng)

        return returnDict

    @property
    def address(self):
        return '%s, %s %s, %s' % (self.street, self.city, self.state, self.zip_code)


def update_date_modified(mapper, connection, target):  # pylint: disable=unused-argument
    # 'target' is the inserted object
    target.date_modified = dt.now().isoformat()  # Update Date Modified


event.listen(School, 'before_update', update_date_modified)
