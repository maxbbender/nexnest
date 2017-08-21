
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

from pprint import pprint
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


    directMessage = notification.Notification.query.filter_by(user=landlordUser, category='direct_message').all()

    genericMessage = notification.Notification.query.filter_by(user=landlordUser, category='generic_message').all()

    print(directMessage)
    print(genericMessage)
