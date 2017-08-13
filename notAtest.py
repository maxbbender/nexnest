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
from sqlalchemy import func, asc, or_, and_

from dateutil import parser

import json

import datetime

gmaps = googlemaps.Client(key='AIzaSyACeJxqY35gOjqNTIukZb6A6Zh6jvQnY3w')

landlord = user.User.query.filter_by(id=1).first()
otherUser = user.User.query.filter_by(id=7).first()

tour = tour.Tour.query.filter_by(id=7).first()

print(tour.genTourEmailCreatedContent(user=otherUser))
