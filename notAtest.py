from nexnest.application import app, session, db
from sqlalchemy import desc, or_

from nexnest.models import *
from nexnest.models.base import Base
from nexnest.models.notification import Notification


from nexnest import logger

import os
import re
import datetime

from pprint import pprint
from nexnest.utils.school import allSchoolsAsStrings
import googlemaps

user = user.User.query.filter_by(id=1).first()
print(user.getNotifications())

for notif in user.getNotifications():
    print("Notif type %s | redirectURL %s" % (notif.notif_type, notif.redirect_url))

print('message')
for notif in user.getMessageNotifications():
    print("Notif type %s | redirectURL %s" % (notif.notif_type, notif.redirect_url))

# print("All Notifications for user 1")
# allNotifs = Notification.query.filter_by(target_user_id=1)
# print(allNotifs)
# for notif in allNotifs:
#     print("Notif type %s | redirectURL %s" % (notif.notif_type, notif.redirect_url))


# allDistinctNotifs = Notification.query.filter_by(target_user_id=1).distinct(Notification.redirect_url, Notification.notif_type)
# print(allNotifs)
# for notif in allDistinctNotifs:
#     print("Notif type %s | redirectURL %s" % (notif.notif_type, notif.redirect_url))

# allNotifications = session.query(Notification.redirect_url,
#                                  Notification.notif_type) \
#     .filter_by(target_user_id=1) \
#     .group_by(Notification.redirect_url, Notification.notif_type) \
#     .paginate(1, 10, False).items

# allNotifications = Notification.query.paginate(2,3,False)
# allNotifications = Base.Notification.query.paginate(1,3,False)

# print(type(Notification.query))
# print(Notification.query)
# # print(type(db.session.Notification.query))
# print(allNotifications)
