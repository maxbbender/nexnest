from nexnest.application import app, session
from sqlalchemy import desc

from nexnest.models import *

import os

u = session.query(listing.Listing).filter_by(id=1).first()
print(u)

print(u.hasPets)