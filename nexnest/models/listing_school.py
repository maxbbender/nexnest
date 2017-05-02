import math

from sqlalchemy.orm import relationship

import googlemaps

from pprint import pformat

from nexnest import logger
from nexnest.application import db

from nexnest.models.base import Base


class ListingSchool(Base):
    __tablename__ = 'listing_schools'
    listing_id = db.Column(db.Integer,
                           db.ForeignKey('listings.id'),
                           primary_key=True)

    school_id = db.Column(db.Integer,
                          db.ForeignKey('schools.id'),
                          primary_key=True)
    # destination_address = db.Column(db.Text)
    # origin_address = db.Column(db.Text)
    driving_time = db.Column(db.Numeric)  # In Minutes
    driving_miles = db.Column(db.Numeric)  # In Miles
    walking_time = db.Column(db.Numeric)  # In Minutes
    walking_miles = db.Column(db.Numeric)  # In Miles

    school = relationship('School', back_populates='listings')
    listing = relationship('Listing', back_populates='schools')

    def __init__(
            self,
            listing,
            school,
            driving_time=None,
            driving_miles=None,
            walking_time=None,
            walking_miles=None
    ):
        self.listing = listing
        self.school = school

        # First lest see if this has already been calculated for this listing address
        gmaps = googlemaps.Client(key='AIzaSyACeJxqY35gOjqNTIukZb6A6Zh6jvQnY3w')

        if driving_time is None or driving_miles is None:
            drivingResponse = gmaps.distance_matrix(origins=self.listing.address,
                                                    destinations=self.school.address,
                                                    units='imperial')
            logger.debug("Driving Response")
            logger.debug(pformat(drivingResponse))

            if drivingResponse['status'] == 'OK' and drivingResponse['rows'][0]['elements'][0]['status'] == 'OK':
                self.driving_time = math.ceil((drivingResponse['rows'][0]['elements'][0]['duration']['value']) / 60)
                self.driving_miles = round((drivingResponse['rows'][0]['elements'][0]['distance']['value'] / 1609.34), 1)
            else:
                logger.warning('Could not calculate driving time from %r to %r' % (self.listing, self.school))
                logger.warning('Status from googlemaps : %s' % drivingResponse['status'])
        else:
            self.driving_time = driving_time
            self.driving_miles = driving_miles

        if walking_time is None or walking_miles is None:
            walkingResponse = gmaps.distance_matrix(origins=self.listing.address,
                                                    destinations=self.school.address,
                                                    units='imperial',
                                                    mode='walking')

            logger.debug("Walking Response")
            logger.debug(pformat(walkingResponse))

            if walkingResponse['status'] == 'OK' and walkingResponse['rows'][0]['elements'][0]['status'] == 'OK':
                self.walking_time = math.ceil(walkingResponse['rows'][0]['elements'][0]['duration']['value'] / 60)
                self.walking_miles = round((walkingResponse['rows'][0]['elements'][0]['distance']['value'] / 1609.34), 1)
            else:
                logger.warning('Could not calculate walking time from %r to %r' % (self.listing, self.school))
                logger.warning('Status from googlemaps : %s' % walkingResponse['status'])
        else:
            self.walking_miles = walking_miles
            self.walking_time = walking_time

    def __repr__(self):
        return '<School %r | Listing %r>' % (self.school, self.listing)
