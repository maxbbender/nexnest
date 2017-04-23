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

# print(90* (1 - (10/100)))
# send_email('Dom', 'no_reply@nexnest.com', ['maxbbender@gmail.com'], 'Hey You', None)
user = user.User.query.first()
print(user)

emailSend = user.sendEmail(emailType='message', message='domislove')
print(emailSend)
