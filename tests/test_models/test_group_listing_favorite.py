import unittest

from nexnest.application import session

from nexnest.data_gen.factories import UserFactory, GroupFactory, GroupUserFactory, ListingFactory, LandlordListingFactory, LandlordFactory, GroupListingFavoriteFactory

from nexnest.models.notification import Notification

from .utils import dropAllRows


class TestGroupListingFavorite(unittest.TestCase):

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

        self.glf = GroupListingFavoriteFactory(group=self.group, listing=self.listing, user=self.leader)

        session.commit()

        self.glf.genNotifications()

    def tearDown(self):
        dropAllRows()

    def testNotifications(self):
        # We should see 4 notifications for this group listing favorite
        notifCount = session.query(Notification) \
            .filter_by(notif_type='group_listing_favorite',
                       target_model_id=self.glf.id) \
            .count()

        self.assertEqual(notifCount, 4)
