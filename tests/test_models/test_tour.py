import unittest

from nexnest.application import session

from nexnest.data_gen.factories import UserFactory, GroupFactory, GroupUserFactory, ListingFactory, LandlordListingFactory, LandlordFactory, TourFactory, TourMessageFactory

from nexnest.models.notification import Notification
from nexnest.models.notification_preference import NotificationPreference

from .utils import dropAllRows


class TestTour(unittest.TestCase):

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

        for landlord in self.tour.listing.landLordsAsUsers():
            notifCount = session.query(Notification) \
                .filter_by(notif_type='tour',
                           target_model_id=self.tour.id,
                           target_user_id=landlord.id) \
                .count()

            self.assertEqual(notifCount, 1)

    def testTourConfirmNotifications(self):
        self.tour.genConfirmNotifications()

        for user in self.tour.group.acceptedUsers:
            notifCount = session.query(Notification) \
                .filter_by(notif_type='tour_confirmed',
                           target_model_id=self.tour.id,
                           target_user_id=user.id) \
                .count()

            self.assertEqual(notifCount, 1)

        self.tour.undoConfirmNotifications()

        notifCount = session.query(Notification) \
            .filter_by(notif_type='tour_confirmed',
                       target_model_id=self.tour.id) \
            .count()

        self.assertEqual(notifCount, 0)

    def testTourDeniedNotifications(self):
        self.tour.genDeniedNotifications()

        for user in self.tour.group.acceptedUsers:
            notifCount = session.query(Notification) \
                .filter_by(notif_type='tour_denied',
                           target_model_id=self.tour.id,
                           target_user_id=user.id) \
                .count()

            self.assertEqual(notifCount, 1)

        self.tour.undoDeniedNotifications()

        notifCount = session.query(Notification) \
            .filter_by(notif_type='tour_denied',
                       target_model_id=self.tour.id) \
            .count()

        self.assertEqual(notifCount, 0)

    def testTourTimeChangeNotifications(self):
        self.tour.last_requested = 'landlord'
        session.commit()

        print("Last Requested : %s" % self.tour.last_requested)
        self.tour.genTimeChangeNotifications()

        newTourTimeNotifs = session.query(Notification).filter_by(notif_type='new_tour_time').all()
        print(newTourTimeNotifs)

        for user in self.tour.group.acceptedUsers:
            notifCount = session.query(Notification) \
                .filter_by(notif_type='new_tour_time',
                           target_model_id=self.tour.id,
                           target_user_id=user.id) \
                .count()

            self.assertEqual(notifCount, 1)

        self.tour.undoTimeChangeNotifications()

        notifCount = session.query(Notification) \
            .filter_by(notif_type='new_tour_time',
                       target_model_id=self.tour.id) \
            .count()

        self.assertEqual(notifCount, 0)

    def testTourMessageNotifications(self):
        newTM = TourMessageFactory(user=self.leader,
                                   tour=self.tour)
        session.add(newTM)
        session.commit()

        newTM.genNotifications()

        allTMNotifs = session.query(Notification).filter_by(notif_type='tour_message').all()
        print("All TM Notifications %r" % allTMNotifs)

        for user in self.tour.group.acceptedUsers:
            if user is not self.leader:
                notifCount = session.query(Notification) \
                    .filter_by(notif_type='tour_message',
                               target_model_id=newTM.id,
                               target_user_id=user.id) \
                    .count()

                self.assertEqual(notifCount, 1)

        for user in self.tour.listing.landLordsAsUsers():
            notifCount = session.query(Notification) \
                .filter_by(notif_type='tour_message',
                           target_model_id=newTM.id,
                           target_user_id=user.id) \
                .count()

            self.assertEqual(notifCount, 1)

        newLandlordTM = TourMessageFactory(user=self.landlordUser,
                                           tour=self.tour)
        session.add(newLandlordTM)
        session.commit()

        newLandlordTM.genNotifications()

        for user in self.tour.group.acceptedUsers:
            notifCount = session.query(Notification) \
                .filter_by(notif_type='tour_message',
                           target_model_id=newLandlordTM.id,
                           target_user_id=user.id) \
                .count()

            self.assertEqual(notifCount, 1)

        for user in self.tour.listing.landLordsAsUsers():
            if user is not self.landlordUser:
                notifCount = session.query(Notification) \
                    .filter_by(notif_type='tour_message',
                               target_model_id=newLandlordTM.id,
                               target_user_id=user.id) \
                    .count()

                self.assertEqual(notifCount, 1)
