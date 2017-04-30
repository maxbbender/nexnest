import unittest

import pprint

from nexnest.application import session

from nexnest.data_gen.factories import UserFactory, GroupFactory, GroupUserFactory, ListingFactory, LandlordListingFactory, LandlordFactory, MaintenanceMessageFactory, HouseFactory, HouseMessageFactory, MaintenanceFactory

from nexnest.models.notification import Notification
from nexnest.models.notification_preference import NotificationPreference

from .utils import dropAllRows

pp = pprint.PrettyPrinter(indent=4)


class TestHouse(unittest.TestCase):

    def setUp(self):
        self.landlordUser = UserFactory()
        session.commit()

        newNotifPref = NotificationPreference(user=self.landlordUser)
        session.add(newNotifPref)
        session.commit()

        self.leader = UserFactory()
        session.commit()

        newNotifPref = NotificationPreference(user=self.leader)
        session.add(newNotifPref)
        session.commit()

        self.landlord = LandlordFactory(user=self.landlordUser)
        session.commit()

        self.group = GroupFactory(leader=self.leader)
        session.commit()

        # Create some group users
        for i in range(4):
            u = UserFactory()
            session.commit()

            newNotifPref = NotificationPreference(user=u)
            session.add(newNotifPref)
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

        for user in self.house.listing.landLordsAsUsers():
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

    def testMaintenanceMessageNotifications(self):
        newMaintenance = MaintenanceFactory(house=self.house, user=self.leader)
        session.commit()

        newMaintenanceMessage = MaintenanceMessageFactory(maintenance=newMaintenance, user=self.leader)
        session.commit()

        newMaintenanceMessage.genNotifications()

        notifications = session.query(Notification).filter_by(notif_type='maintenance_message', target_model_id=newMaintenanceMessage.id).all()

        pp.pprint(notifications)
        print(notifications)

        for user in self.house.tenants:
            if user is not self.leader:
                notifCount = session.query(Notification) \
                    .filter_by(notif_type='maintenance_message',
                               target_model_id=newMaintenanceMessage.id,
                               target_user_id=user.id) \
                    .count()

                self.assertEqual(notifCount, 1)

        for landlord in self.house.listing.landLordsAsUsers():
            notifCount = session.query(Notification) \
                .filter_by(notif_type='maintenance_message',
                           target_model_id=newMaintenanceMessage.id,
                           target_user_id=landlord.id) \
                .count()

            self.assertEqual(notifCount, 1)

    def testMaintenanceInProgressNotifications(self):
        newMaintenance = MaintenanceFactory(house=self.house, user=self.leader)
        session.commit()

        newMaintenance.genInProgressNotifications()

        for user in self.house.tenants:
            notifCount = session.query(Notification) \
                .filter_by(notif_type='maintenance_inprogress',
                           target_model_id=newMaintenance.id,
                           target_user_id=user.id) \
                .count()

            self.assertEqual(notifCount, 1)

        # Now we undo them as if an ajax request came in
        newMaintenance.removeInProgressNotifications()

        for user in self.house.tenants:
            notifCount = session.query(Notification) \
                .filter_by(notif_type='maintenance_inprogress',
                           target_model_id=newMaintenance.id,
                           target_user_id=user.id) \
                .count()

            self.assertEqual(notifCount, 0)

    def testMaintenanceCompletedNotifications(self):
        newMaintenance = MaintenanceFactory(house=self.house, user=self.leader)
        session.commit()

        newMaintenance.genCompletedNotifications()

        for user in self.house.tenants:
            notifCount = session.query(Notification) \
                .filter_by(notif_type='maintenance_completed',
                           target_model_id=newMaintenance.id,
                           target_user_id=user.id) \
                .count()

            self.assertEqual(notifCount, 1)

        # Now we undo them as if an ajax request came in
        newMaintenance.removeCompletedNotifications()
        for user in self.house.tenants:
            notifCount = session.query(Notification) \
                .filter_by(notif_type='maintenance_completed',
                           target_model_id=newMaintenance.id,
                           target_user_id=user.id) \
                .count()

            self.assertEqual(notifCount, 0)

