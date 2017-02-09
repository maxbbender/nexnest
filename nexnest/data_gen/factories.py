from nexnest.application import session

from nexnest.models.user import User
from nexnest.models.listing import Listing
from nexnest.models.landlord import Landlord
from nexnest.models.landlord_listing import LandlordListing
from nexnest.models.group import Group
from nexnest.models.group_user import GroupUser
from nexnest.models.group_listing import GroupListing
from nexnest.models.group_listing_message import GroupListingMessage
from nexnest.models.message import Message
from nexnest.models.group_message import GroupMessage
from nexnest.models.school import School
from nexnest.models.direct_message import DirectMessage
from nexnest.models.tour import Tour
from nexnest.models.tour_message import TourMessage
from nexnest.models.house import House
from nexnest.models.house_message import HouseMessage
from nexnest.models.security_deposit import SecurityDeposit
from nexnest.models.maintenance import Maintenance
from nexnest.models.maintenance_message import MaintenanceMessage

import factory
from faker import Faker

from datetime import date

import random

from nexnest.static.dataSets import maintenanceRequestTypes

fake = Faker()


class SchoolFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = School
        sqlalchemy_session = session

    name = factory.LazyAttribute(lambda x: fake.company())
    street = factory.LazyAttribute(lambda x: fake.street_address())
    city = factory.LazyAttribute(lambda x: fake.city())
    state = factory.LazyAttribute(lambda x: fake.state_abbr())
    zip_code = factory.LazyAttribute(lambda x: fake.zipcode())
    phone = '1234567890'


class UserFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = User
        sqlalchemy_session = session

    email = factory.Sequence(lambda x: u'fake%d@fake.com' % x)
    password = 'domislove'
    fname = factory.LazyAttribute(lambda x: fake.first_name())
    lname = factory.LazyAttribute(lambda x: fake.last_name())
    school = factory.SubFactory(SchoolFactory)
    role = 'user'


class ListingFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Listing
        sqlalchemy_session = session

    street = factory.LazyAttribute(lambda x: fake.street_address())
    city = factory.LazyAttribute(lambda x: fake.city())
    state = factory.LazyAttribute(lambda x: fake.state_abbr())
    zip_code = factory.LazyAttribute(lambda x: fake.zipcode())
    start_date = factory.LazyAttribute(lambda x: fake.date(pattern="%Y-%m-%d"))
    end_date = factory.LazyAttribute(lambda x: fake.date(pattern="%Y-%m-%d"))
    unit_type = 'apartment'
    num_bedrooms = 3
    price = 6000
    square_footage = 3500
    parking = 'onstreet'
    cats = False
    dogs = True
    other_pets = False
    washer = True
    dryer = True
    dishwasher = True
    air_conditioning = True
    handicap = True
    furnished = False
    utilities_included = False
    emergency_maintenance = False
    snow_plowing = True
    garbage_service = True
    security_service = True
    description = factory.LazyAttribute(lambda x: fake.paragraph())
    num_half_baths = 4
    num_full_baths = 3
    time_period = 'semester'
    apartment_number = 2


class LandlordFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Landlord
        sqlalchemy_session = session

    user = factory.SubFactory(UserFactory)
    online_pay = True
    check_pay = True
    street = factory.LazyAttribute(lambda x: fake.street_address())
    city = factory.LazyAttribute(lambda x: fake.city())
    state = factory.LazyAttribute(lambda x: fake.state_abbr())
    zip_code = factory.LazyAttribute(lambda x: fake.zipcode())


class LandlordListingFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = LandlordListing
        sqlalchemy_session = session

    landlord = factory.SubFactory(LandlordFactory)
    listing = factory.SubFactory(ListingFactory)


class GroupFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Group
        sqlalchemy_session = session

    name = factory.LazyAttribute(lambda x: fake.company())
    leader = factory.SubFactory(UserFactory)
    start_date = date.today()
    end_date = date(date.today().year + 1,
                    date.today().month,
                    date.today().day)


class GroupUserFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = GroupUser
        sqlalchemy_session = session

    group = factory.SubFactory(GroupFactory)
    user = factory.SubFactory(UserFactory)


class GroupListingFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = GroupListing
        sqlalchemy_session = session

    group = factory.SubFactory(GroupFactory)
    listing = factory.SubFactory(ListingFactory)


class MessageFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Message
        sqlalchemy_session = session

    content = factory.LazyAttribute(lambda x: fake.paragraph())
    user = factory.SubFactory(UserFactory)


class GroupMessageFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = GroupMessage
        sqlalchemy_session = session

    group = factory.SubFactory(GroupFactory)
    content = factory.LazyAttribute(lambda x: fake.paragraph(3))
    user = factory.SubFactory(UserFactory)


class DirectMessageFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = DirectMessage
        sqlalchemy_session = session

    source_user = factory.SubFactory(UserFactory)
    target_user = factory.SubFactory(UserFactory)
    content = factory.LazyAttribute(lambda x: fake.paragraph(3))


class TourFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Tour
        sqlalchemy_session = session

    listing = factory.SubFactory(ListingFactory)
    group = factory.SubFactory(GroupFactory)
    time_requested = factory.LazyAttribute(lambda x: fake.date_time())


class TourMessageFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = TourMessage
        sqlalchemy_session = session

    tour = factory.SubFactory(TourFactory)
    content = factory.LazyAttribute(lambda x: fake.paragraph(3))
    user = factory.SubFactory(UserFactory)


class GroupListingMessageFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = GroupListingMessage
        sqlalchemy_session = session

    groupListing = factory.SubFactory(GroupListingFactory)
    content = factory.LazyAttribute(lambda x: fake.paragraph(3))
    user = factory.SubFactory(UserFactory)


class HouseFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = House
        sqlalchemy_session = session

    listing = factory.SubFactory(ListingFactory)
    group = factory.SubFactory(Group)


class HouseMessageFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = HouseMessage
        sqlalchemy_session = session

    house = factory.SubFactory(HouseFactory)
    content = factory.LazyAttribute(lambda x: fake.paragraph(3))
    user = factory.SubFactory(UserFactory)


class SecurityDepositFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = SecurityDeposit
        sqlalchemy_session = session

    groupListing = factory.SubFactory(GroupListingFactory)
    user = factory.SubFactory(UserFactory)


class MaintenanceFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Maintenance
        sqlalchemy_session = session

    request_type = random.choice(maintenanceRequestTypes)[0]
    details = factory.LazyAttribute(lambda x: fake.paragraph(3))
    house = factory.SubFactory(HouseFactory)


class MaintenanceMessageFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = MaintenanceMessage
        sqlalchemy_session = session

    maintenance = factory.SubFactory(MaintenanceFactory)
    content = factory.LazyAttribute(lambda x: fake.paragraph(3))
    user = factory.SubFactory(UserFactory)
