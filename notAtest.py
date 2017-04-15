from nexnest.application import app, session
from sqlalchemy import desc, or_

from nexnest.models import *

from nexnest import logger

import os
import re
import datetime

from pprint import pprint
from nexnest.utils.school import allSchoolsAsStrings
import googlemaps

notif = session.query(notification.Notification).first()

print(notif.user)