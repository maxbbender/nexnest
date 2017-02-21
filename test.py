from nexnest.application import session, app

from sqlalchemy import desc

from nexnest.models import *

import os


u = session.query(User).filter_by(id=2).first()
print(u)
print(u.unreadNotifications())
