from nexnest.application import app, session
from sqlalchemy import desc

from nexnest.models import *

import os

u2 = session.query(user.User).filter_by(username='fake1').first()

print(u2)

print(u2.unreadNotifications())
dd = u2.unreadNotifications()

for d in dd:
    print (d.type)
u = session.query(direct_message.DirectMessage).filter_by(user_id=3).first()
print(u)
# print(u.notifications.all())

