from nexnest.application import session

from nexnest.models.user import User
from nexnest.models.listing import Listing
from nexnest.models.landlord import Landlord
from nexnest.models.landlord_listing import LandlordListing
from nexnest.models.group import Group
from nexnest.models.group_user import GroupUser
from nexnest.models.group_listing import GroupListing
from nexnest.models.message import Message
from nexnest.models.group_message import GroupMessage

import factory
from faker import Faker

from datetime import date

fake = Faker()


class UserFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = User
        sqlalchemy_session = session

    email = factory.Sequence(lambda x: u'fake%d@fake.com' % x)
    password = 'domislove'
    fname = factory.LazyAttribute(lambda x: fake.first_name())
    lname = factory.LazyAttribute(lambda x: fake.last_name())


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
    description = factory.LazyAttribute(lambda x: fake.sentences(nb=3))
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

    content = factory.LazyAttribute(lambda x: fake.sentences(3))
    user = factory.SubFactory(UserFactory)
    type = 'messages'


class GroupMessageFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = GroupMessage
        sqlalchemy_session = session

    group = factory.SubFactory(GroupFactory)
    message = factory.SubFactory(MessageFactory)
