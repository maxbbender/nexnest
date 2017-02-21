from nexnest.application import session, app

from sqlalchemy import desc
from nexnest.models.group import Group
from nexnest.models.user import User
from nexnest.models.message import Message
from nexnest.models.group_message import GroupMessage
from nexnest.models.direct_message import DirectMessage
from nexnest.models.landlord import Landlord
from nexnest.models.landlord_listing import LandlordListing
from nexnest.models.listing import Listing
from nexnest.models.tour_message import TourMessage
from nexnest.models.group_listing import GroupListing
from nexnest.models.group_listing_message import GroupListingMessage
from nexnest.models.security_deposit import SecurityDeposit
from nexnest.models.maintenance import Maintenance

import os
# tm = session.query(TourMessage).filter_by(tour_id=1).first()
# g = session.query(Group).filter_by(id=1).first()


u = session.query(Listing).filter_by(id=6).first()
print(u.getPhotoURLs())
# print(u.user)
# direct_messages = session.query(DirectMessage.target_user_id) \
#     .filter_by(source_user_id=1) \
#     .order_by(DirectMessage.date_created.desc()) \
#     .all()
# print(direct_messages)

# folderPath = os.path.join(app.config['UPLOAD_FOLDER'], 'listings', '1')
# print(folderPath)

message, model, redirectURL = notification.getNotification()