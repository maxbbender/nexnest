from nexnest.application import app, session
from sqlalchemy import desc

from nexnest.models import *

import os


u = session.query(landlord.Landlord).filter_by(user_id=1).first()
print(u)
requestedTours, scheduledTours = u.getActiveTours()

print('RequestedTours %r' % requestedTours)

print('ScheduledTours %r' % scheduledTours)

un, ac, com = u.getHousingRequests()

print("un %r" % un)
print("ac %r" % ac)
print("comp %r" % com)

print(u.getHouses())

print("Maintenances : %r" % u.getMaintenanceRequests())
