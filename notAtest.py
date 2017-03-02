from nexnest.application import app, session
from sqlalchemy import desc

from nexnest.models import *

import os


u = session.query(landlord.Landlord).filter_by(user_id=1).first()
print(u)
print(u.getMaintenanceRequests())