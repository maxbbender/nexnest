from nexnest.application import session

from nexnest.models.notification import Notification
from nexnest.models.user import User
from nexnest.models.group import Group
from nexnest.models.group_user import GroupUser
from nexnest.models.group_message import GroupMessage
from nexnest.models.message import Message
from nexnest.models.group_listing import GroupListing
from nexnest.models.listing import Listing
from nexnest.models.landlord import Landlord
from nexnest.models.landlord_listing import LandlordListing


def dropAllRows():
    session.query(GroupListing).delete()
    session.commit()
    session.query(GroupMessage).delete()
    session.commit()
    session.query(Message).delete()
    session.commit()
    session.query(GroupUser).delete()
    session.commit()
    session.query(Group).delete()
    session.commit()
    session.query(Notification).delete()
    session.commit()
    session.query(LandlordListing).delete()
    session.commit()
    session.query(Landlord).delete()
    session.commit()
    session.query(User).delete()
    session.commit()
    session.query(Listing).delete()
    session.commit()
