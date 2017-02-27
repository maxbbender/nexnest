from nexnest.application import app, session
from sqlalchemy import desc

from nexnest.models import *

import os

u = session.query(tour_message.TourMessage).filter_by(id=22).first()
print(u)
print(u.tour.group.name)
# print(.notifications.all())

