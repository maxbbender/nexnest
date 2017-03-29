from nexnest.application import app, session
from sqlalchemy import desc

from nexnest.models import *

import os

from pprint import pprint

u = session.query(landlord.Landlord).filter_by(user_id=1).first()
print(u)
pprint(u.getInProgressMaintenanceJSON())

# u = session.query(maintenance.Maintenance).filter_by(id=1).first()
# print(u)
# pprint(u.serialize)

# u = session.query(listing.Listing).filter_by(id=1).first()
# print(u)
# pprint(u.house[0])
