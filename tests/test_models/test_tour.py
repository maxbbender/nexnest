import unittest

from nexnest.application import session

from nexnest.data_gen.factories import UserFactory, GroupFactory, GroupUserFactory, ListingFactory, LandlordListingFactory, LandlordFactory, TourFactory

from nexnest.models.notification import Notification

from .utils import dropAllRows


class TestTour(unittest.TestCase):

    def setUp(self):
        self.landlordUser = UserFactory()
        self.leader = UserFactory()
        session.commit()

        self.landlord = LandlordFactory(user=self.landlordUser)
        session.commit()

        self.group = GroupFactory(leader=self.leader)
        session.commit()

        # Create some group users
        for i in range(4):
            u = UserFactory()
            session.commit()

            gu = GroupUserFactory(user=u, group=self.group)
            gu.accepted = True
            session.commit()

        self.listing = ListingFactory()
        session.commit()

        self.landlordListing = LandlordListingFactory(landlord=self.landlord, listing=self.listing)
        session.commit()

        self.tour = TourFactory(listing=self.listing, group=self.group)
        session.commit()

    def tearDown(self):
        dropAllRows()

    def testTourCreateNotifications(self):
        self.tour.genNotifications()

        for landlord in self.tour.listing.landLordsAsUsers(self):
            notifCount = session.query(Notification) \
                .filter_by(notif_type='tour',
                           target_model_id=self.tour,
                           target_user_id=landlord.id) \
                .count()

            self.assertEqual(notifCount, 1)
