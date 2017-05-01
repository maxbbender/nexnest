from nexnest.application import app, session, db
from sqlalchemy import desc, or_

from nexnest import mail, app
from nexnest.models import *
from nexnest.models.base import Base
from nexnest.models.notification import Notification
from nexnest.utils.email import send_email


from nexnest import logger

import os
import re
import datetime
import googlemaps

from pprint import pprint
from nexnest.utils.school import allSchoolsAsStrings
import googlemaps
from apiclient.discovery import build


user = user.User.query.first()
print(user)

gmaps = googlemaps.Client(key='AIzaSyACeJxqY35gOjqNTIukZb6A6Zh6jvQnY3w')

geocode = gmaps.geocode('117 Bayview Ave, Warwick RI, 02818')
pprint(geocode)
print(geocode[0]['geometry']['location']['lat'])
# geocode = build('geocode', 'v1', developerKey='AIzaSyACeJxqY35gOjqNTIukZb6A6Zh6jvQnY3w')
print(geocode[0]['geometry']['location']['lng'])

