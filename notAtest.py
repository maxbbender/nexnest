from nexnest.application import app, session
from sqlalchemy import desc

from nexnest.models import *

import os

u = session.query(user.User).filter_by(id=1).first()
print(u)

n = u.notifications.group_by(notification.Notification.id, notification.Notification.notif_type, notification.Notification.redirect_url).all()
# n = u.notifications.all()

for f in n:
    print("yo %rAAAA" % f.notif_type)
    print("yo %rAAAAA" % f.redirect_url)

# for f in u:
#     print(f.redirect_url)
