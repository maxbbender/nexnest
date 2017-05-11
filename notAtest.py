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

from dateutil import parser

gmaps = googlemaps.Client(key='AIzaSyACeJxqY35gOjqNTIukZb6A6Zh6jvQnY3w')

user = user.User.query.filter_by(id=2).first()
print(user)

print(os.listdir(os.path.join(app.config['UPLOAD_FOLDER'], 'listings', str(1), 'pictures')))
