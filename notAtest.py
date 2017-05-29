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

import json

gmaps = googlemaps.Client(key='AIzaSyACeJxqY35gOjqNTIukZb6A6Zh6jvQnY3w')

user = user.User.query.filter_by(id=2).first()
print(user)

jsonString = '{"0":["9:00AM","10:00AM","11:00AM","12:00PM","1:00PM","2:00PM","3:00PM","4:00PM","5:00PM","6:00PM","7:00PM"],"1":["10:00AM","1:00PM","2:00PM","3:00PM"],"2":["10:00AM","11:00AM","12:00PM","1:00PM","2:00PM"],"3":["11:00AM","12:00PM","1:00PM","2:00PM","3:00PM"],"4":[],"5":[],"6":[]}'

json = json.loads(jsonString)

pprint(json)
