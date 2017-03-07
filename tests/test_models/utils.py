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
from nexnest.models.group_listing_favorite import GroupListingFavorite
from nexnest.models.house import House
from nexnest.models.house_message import HouseMessage
from nexnest.models.maintenance import Maintenance


def dropAllRows():
    session.query(Maintenance).delete()
    session.commit()
    session.query(HouseMessage).delete()
    session.commit()
    session.query(House).delete()
    session.commit()
    session.query(GroupListingFavorite).delete()
    session.commit()
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
