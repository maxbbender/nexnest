
from sqlalchemy import desc, or_

from nexnest import mail, db, createApp
from nexnest.models import *
from nexnest.models.base import Base
from nexnest.models.notification import Notification
from nexnest.utils.email import send_email


import os
import re
import datetime
import googlemaps

from pprint import pprint, pformat
from nexnest.utils.school import allSchoolsAsStrings
import googlemaps
from apiclient.discovery import build
from sqlalchemy import func, asc, or_, and_

from dateutil import parser

import json

import datetime

app = createApp('default')

with app.app_context():

    gmaps = googlemaps.Client(key='AIzaSyACeJxqY35gOjqNTIukZb6A6Zh6jvQnY3w')

    landlord = landlord.Landlord.query.first()
    landlordUser = landlord.user
    otherUser = user.User.query.filter_by(id=7).first()
    house = house.House.query.filter_by(id=1).first()
    gl = group_listing.GroupListing.query.first()
    # tour = tour.Tour.query.filter_by(id=5).first()
    # maintenancess = maintenance.Maintenance.query.first()

    otherListingsWithSameAddress = listing.Listing.query \
        .filter_by(street='2 Sheldon Drive',
                   city='Poughkeepsie',
                   state='NY',
                   zip_code='12603',
                   apartment_number=1
                   ) \
        .all()

    print (otherListingsWithSameAddress)
