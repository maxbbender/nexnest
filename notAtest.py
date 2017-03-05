from nexnest.application import app, session
from sqlalchemy import desc

from nexnest.models import *

import os


u = session.query(user.User).filter_by(id=1).first()
print(u)

m, n = u.unreadNotifications()

print("Messages %r" % m)
print("not %r" % n)
