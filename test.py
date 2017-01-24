from nexnest.application import session

from nexnest.models.group import Group
from nexnest.models.user import User
from nexnest.models.message import Message
from nexnest.models.group_message import GroupMessage
from nexnest.models.direct_message import DirectMessage
from nexnest.models.landlord import Landlord
from nexnest.models.landlord_listing import LandlordListing
from nexnest.models.listing import Listing

from nexnest.data_gen.factories import GroupFactory, UserFactory

from sqlalchemy import asc, or_, and_

listing = session.query(Listing).filter_by(id=1).first()

print(listing.landlords)

landlordListingArray = listing.landlords

for landlordListing in landlordListingArray:
    print (landlordListing.landlord.user.fname)
    print (landlordListing.listing.street)
