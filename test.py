from nexnest.application import app, session
from sqlalchemy import desc

from nexnest.models import *

import os


u = session.query(Notification).filter_by(id=2).first()
print(u)
print(u.message)
print(u.redirectURL)
print(u.returnObject)
