from nexnest.application import app, session, db
from sqlalchemy import desc, or_

from nexnest import mail
from nexnest.models import *
from nexnest.models.base import Base
from nexnest.models.notification import Notification
from nexnest.utils.email import send_email


from nexnest import logger

import os
import re
import datetime

from pprint import pprint
from nexnest.utils.school import allSchoolsAsStrings
import googlemaps

user = user.User.query.first()
print(user)

print(user.getUnreadNotificationCount())
