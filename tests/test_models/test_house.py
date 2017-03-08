import unittest

from nexnest.application import session

from nexnest.data_gen.factories import UserFactory, GroupFactory, GroupUserFactory, ListingFactory, LandlordListingFactory, LandlordFactory, HouseFactory, HouseMessageFactory, MaintenanceFactory

from nexnest.models.notification import Notification

from .utils import dropAllRows


class TestHouse(unittest.TestCase):

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

        self.house = HouseFactory(listing=self.listing,
                                  group=self.group)
        session.commit()

    def tearDown(self):
        dropAllRows()

    def testHouseMessageNotifications(self):
        # There is a new message
        newHM = HouseMessageFactory(house=self.house,
                                    user=self.leader)

        session.commit()

        newHM.genNotifications()

        for user in self.house.tenants:
            if user is not self.leader:
                notifCount = session.query(Notification) \
                    .filter_by(notif_type='house_message',
                               target_model_id=newHM.id,
                               target_user_id=user.id) \
                    .count()

                self.assertEqual(notifCount, 1)

    def testMaintenanceNotifications(self):
        newMaintenance = MaintenanceFactory(house=self.house, user=self.leader)
        session.commit()

        newMaintenance.genNotifications()

        for user in self.house.tenants:
            if user is not self.leader:
                notifCount = session.query(Notification) \
                    .filter_by(notif_type='maintenance',
                               target_model_id=newMaintenance.id,
                               target_user_id=user.id) \
                    .count()

                self.assertEqual(notifCount, 1)
