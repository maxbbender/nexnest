# pylint: disable=E0602

from nexnest.application import session
from nexnest.models import *
from nexnest.static.dataSets import maintenanceRequestTypes, notificationTypes

import factory
from factory.fuzzy import FuzzyInteger
from faker import Faker

from datetime import date

import random


fake = Faker()

fredonia = session.query(school.School).filter_by(name='SUNY at Fredonia').first()


class SchoolFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = school.School
        sqlalchemy_session = session

    name = factory.LazyAttribute(lambda x: fake.company())
    street = factory.LazyAttribute(lambda x: fake.street_address())
    city = factory.LazyAttribute(lambda x: fake.city())
    state = factory.LazyAttribute(lambda x: fake.state_abbr())
    zip_code = factory.LazyAttribute(lambda x: fake.zipcode())
    phone = '1234567890'


class UserFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = user.User
        sqlalchemy_session = session

    email = factory.Sequence(lambda x: u'fake%d@fake.com' % x)
    password = 'domislove'
    fname = factory.LazyAttribute(lambda x: fake.first_name())
    lname = factory.LazyAttribute(lambda x: fake.last_name())
    school = factory.SubFactory(SchoolFactory)
    role = 'user'
    email_confirmed = True


class ListingFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = listing.Listing
        sqlalchemy_session = session

    street = factory.LazyAttribute(lambda x: fake.street_address())
    city = factory.LazyAttribute(lambda x: fake.city())
    state = factory.LazyAttribute(lambda x: fake.state_abbr())
    zip_code = factory.LazyAttribute(lambda x: fake.zipcode())
    start_date = factory.LazyAttribute(lambda x: fake.date(pattern="%Y-%m-%d"))
    end_date = factory.LazyAttribute(lambda x: fake.date(pattern="%Y-%m-%d"))
    num_bedrooms = FuzzyInteger(1,6)
    price = FuzzyInteger(1000,6000, 100)
    square_footage = FuzzyInteger(1000,6000, 100)
    parking = 'onstreet'
    cats = factory.LazyAttribute(lambda x: fake.boolean(chance_of_getting_true=50))
    dogs = factory.LazyAttribute(lambda x: fake.boolean(chance_of_getting_true=50))
    other_pets = factory.LazyAttribute(lambda x: fake.paragraph(nb_sentences=2))
    washer = factory.LazyAttribute(lambda x: fake.boolean(chance_of_getting_true=50))
    dryer = factory.LazyAttribute(lambda x: fake.boolean(chance_of_getting_true=50))
    dishwasher = factory.LazyAttribute(lambda x: fake.boolean(chance_of_getting_true=50))
    air_conditioning = factory.LazyAttribute(lambda x: fake.boolean(chance_of_getting_true=50))
    handicap = factory.LazyAttribute(lambda x: fake.boolean(chance_of_getting_true=50))
    furnished = factory.LazyAttribute(lambda x: fake.boolean(chance_of_getting_true=50))
    emergency_maintenance = factory.LazyAttribute(lambda x: fake.boolean(chance_of_getting_true=50))
    snow_plowing = factory.LazyAttribute(lambda x: fake.boolean(chance_of_getting_true=50))
    garbage_service = factory.LazyAttribute(lambda x: fake.boolean(chance_of_getting_true=50))
    security_service = factory.LazyAttribute(lambda x: fake.boolean(chance_of_getting_true=50))
    description = factory.LazyAttribute(lambda x: fake.paragraph())
    num_half_baths = FuzzyInteger(1,2)
    num_full_baths = FuzzyInteger(1,4)
    time_period = 'school'
    apartment_number = 2
    property_type = 'apartment'
    rent_due = 'semester'
    first_semester_rent_due_date = factory.LazyAttribute(
        lambda x: fake.date(pattern="%Y-%m-%d"))
    second_semester_rent_due_date = factory.LazyAttribute(
        lambda x: fake.date(pattern="%Y-%m-%d"))
    # monthly_rent_due_date = factory.LazyAttribute(lambda x: fake.date(pattern="%Y-%m-%d"))
    electricity = factory.LazyAttribute(lambda x: fake.boolean(chance_of_getting_true=50))
    internet = factory.LazyAttribute(lambda x: fake.boolean(chance_of_getting_true=50))
    water = factory.LazyAttribute(lambda x: fake.boolean(chance_of_getting_true=50))
    heat_gas = factory.LazyAttribute(lambda x: fake.boolean(chance_of_getting_true=50))
    cable = factory.LazyAttribute(lambda x: fake.boolean(chance_of_getting_true=50))
    washer_free = factory.LazyAttribute(lambda x: fake.boolean(chance_of_getting_true=50))
    youtube_url = 'https://www.youtube.com/watch?v=dQw4w9WgXcQ'
    time_period_date_range = '2017-2018'


class LandlordFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = landlord.Landlord
        sqlalchemy_session = session

    user = factory.SubFactory(UserFactory)
    online_pay = factory.LazyAttribute(lambda x: fake.boolean(chance_of_getting_true=50))
    check_pay = factory.LazyAttribute(lambda x: fake.boolean(chance_of_getting_true=50))
    street = factory.LazyAttribute(lambda x: fake.street_address())
    city = factory.LazyAttribute(lambda x: fake.city())
    state = factory.LazyAttribute(lambda x: fake.state_abbr())
    zip_code = factory.LazyAttribute(lambda x: fake.zipcode())


class LandlordListingFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = landlord_listing.LandlordListing
        sqlalchemy_session = session

    landlord = factory.SubFactory(LandlordFactory)
    listing = factory.SubFactory(ListingFactory)


class GroupFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = group.Group
        sqlalchemy_session = session

    name = factory.LazyAttribute(lambda x: fake.company())
    leader = factory.SubFactory(UserFactory)
    # start_date = date.today()
    # end_date = date(date.today().year + 1,
    #                 date.today().month,
    #                 date.today().day)
    target_time_period = '2017-2018'


class GroupUserFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = group_user.GroupUser
        sqlalchemy_session = session

    group = factory.SubFactory(GroupFactory)
    user = factory.SubFactory(UserFactory)


class GroupListingFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = group_listing.GroupListing
        sqlalchemy_session = session

    group = factory.SubFactory(GroupFactory)
    listing = factory.SubFactory(ListingFactory)


class MessageFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = message.Message
        sqlalchemy_session = session

    content = factory.LazyAttribute(lambda x: fake.paragraph())
    user = factory.SubFactory(UserFactory)


class GroupMessageFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = group_message.GroupMessage
        sqlalchemy_session = session

    group = factory.SubFactory(GroupFactory)
    content = factory.LazyAttribute(lambda x: fake.paragraph(3))
    user = factory.SubFactory(UserFactory)


class DirectMessageFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = direct_message.DirectMessage
        sqlalchemy_session = session

    source_user = factory.SubFactory(UserFactory)
    target_user = factory.SubFactory(UserFactory)
    content = factory.LazyAttribute(lambda x: fake.paragraph(3))


class TourFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = tour.Tour
        sqlalchemy_session = session

    listing = factory.SubFactory(ListingFactory)
    group = factory.SubFactory(GroupFactory)
    time_requested = factory.LazyAttribute(
        lambda x: fake.date_time_this_year(before_now=False, after_now=True))


class TourMessageFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = tour_message.TourMessage
        sqlalchemy_session = session

    tour = factory.SubFactory(TourFactory)
    content = factory.LazyAttribute(lambda x: fake.paragraph(3))
    user = factory.SubFactory(UserFactory)


class GroupListingMessageFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = group_listing_message.GroupListingMessage
        sqlalchemy_session = session

    groupListing = factory.SubFactory(GroupListingFactory)
    content = factory.LazyAttribute(lambda x: fake.paragraph(3))
    user = factory.SubFactory(UserFactory)


class HouseFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = house.House
        sqlalchemy_session = session

    listing = factory.SubFactory(ListingFactory)
    group = factory.SubFactory(GroupFactory)


class HouseMessageFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = house_message.HouseMessage
        sqlalchemy_session = session

    house = factory.SubFactory(HouseFactory)
    content = factory.LazyAttribute(lambda x: fake.paragraph(3))
    user = factory.SubFactory(UserFactory)


class SecurityDepositFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = security_deposit.SecurityDeposit
        sqlalchemy_session = session

    groupListing = factory.SubFactory(GroupListingFactory)
    user = factory.SubFactory(UserFactory)


class MaintenanceFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = maintenance.Maintenance
        sqlalchemy_session = session

    request_type = random.choice(maintenanceRequestTypes)[0]
    details = factory.LazyAttribute(lambda x: fake.paragraph(3))
    house = factory.SubFactory(HouseFactory)
    user = factory.SubFactory(UserFactory)


class MaintenanceMessageFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = maintenance_message.MaintenanceMessage
        sqlalchemy_session = session

    maintenance = factory.SubFactory(MaintenanceFactory)
    content = factory.LazyAttribute(lambda x: fake.paragraph(3))
    user = factory.SubFactory(UserFactory)


class NotificationFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = notification.Notification
        sqlalchemy_session = session

    target_user = factory.SubFactory(UserFactory)
    target_model_id = -1
    notif_type = random.choice(notificationTypes)


class GroupListingFavoriteFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = group_listing_favorite.GroupListingFavorite
        sqlalchemy_session = session

    group = factory.SubFactory(GroupFactory)
    listing = factory.SubFactory(ListingFactory)
    user = factory.SubFactory(UserFactory)


class CouponFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = coupon.Coupon
        sqlalchemy_session = session

    coupon_key = None
    unlimited = False
    uses = 10
    percentage_off = 0


class ListingSchoolFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = listing_school.ListingSchool
        sqlalchemy_session = session

    listing = factory.SubFactory(ListingFactory)
    school = fredonia
    driving_time = FuzzyInteger(3,20)
    driving_miles = FuzzyInteger(1,5)
    walking_time = FuzzyInteger(5,25)
    walking_miles = FuzzyInteger(1,10)


class NotificationPreferenceFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = notification_preference.NotificationPreference
        sqlalchemy_session = session

    user = factory.SubFactory(UserFactory)
