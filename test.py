from nexnest.application import app, session
from sqlalchemy import desc

from nexnest.models import *

import os


u = session.query(landlord.Landlord).filter_by(user_id=1).first()
print(u)
print("tours %r" % u.getActiveTours())
print(u.getHousingRequests())
un, ac, com = u.getHousingRequests()

print("un %r" % un)
print("ac %r" % ac)
print("comp %r" % com)
