from nexnest.application import app, session, db
from sqlalchemy import desc, or_

from nexnest.models import *
from nexnest.models.base import Base
from nexnest.models.notification import Notification


from nexnest import logger

import os
import re
import datetime

from pprint import pprint
from nexnest.utils.school import allSchoolsAsStrings
import googlemaps

        
# allNotifications = Notification.query.paginate(1,3,False)
# allNotifications = Base.Notification.query.paginate(1,3,False)

print(type(Notification.query))
print(type(db.session.Notification.query))