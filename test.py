from nexnest.application import session

from nexnest.models.group import Group
from nexnest.models.user import User
from nexnest.models.message import Message
from nexnest.models.group_message import GroupMessage
from nexnest.models.direct_message import DirectMessage
from nexnest.models.landlord import Landlord
from nexnest.models.landlord_listing import LandlordListing
from nexnest.models.listing import Listing
from nexnest.models.tour_message import TourMessage

from nexnest.data_gen.factories import GroupFactory, UserFactory

from sqlalchemy import asc, or_, and_

# tm = session.query(TourMessage).filter_by(tour_id=1).first()
# g = session.query(Group).filter_by(id=1).first()


u = session.query(User).filter_by(id=2).first()

print(u.isGroupLeader)