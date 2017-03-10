import unittest

from nexnest.application import session

from nexnest.data_gen.factories import UserFactory, GroupFactory, GroupUserFactory, ListingFactory, LandlordListingFactory, LandlordFactory, GroupListingMessageFactory

from nexnest.models.notification import Notification
# from nexnest.models.user import User
# from nexnest.models.group import Group
# from nexnest.models.group_user import GroupUser
# from nexnest.models.group_message import GroupMessage
# from nexnest.models.message import Message
from nexnest.models.group_listing import GroupListing

from .utils import dropAllRows


class TestGroupListing(unittest.TestCase):

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

        # The leader creates a new listing request
        self.gl = GroupListing(group=self.group, listing=self.listing)
        session.commit()

        self.gl.genNotifications()

    def tearDown(self):
        dropAllRows()

    def testGroupListingNotifications(self):
        for landlord in self.listing.landLordsAsUsers():
            notifCount = session.query(Notification) \
                .filter_by(notif_type='group_listing',
                           target_model_id=self.gl.id,
                           target_user_id=landlord.id) \
                .count()

            self.assertEqual(notifCount, 1)

    def testGroupListingMessageNotifications(self):
        newGLM = GroupListingMessageFactory(groupListing=self.gl,
                                            user=self.leader)
        session.commit()

        newGLM.genNotifications()

        for user in self.gl.group.acceptedUsers:
            if user is not self.leader:
                notifCount = session.query(Notification) \
                    .filter_by(notif_type='group_listing_message',
                               target_model_id=newGLM.id,
                               target_user_id=user.id) \
                    .count()

                self.assertEqual(notifCount, 1)

        for user in self.gl.listing.landLordsAsUsers():
            notifCount = session.query(Notification) \
                .filter_by(notif_type='group_listing_message',
                           target_model_id=newGLM.id,
                           target_user_id=user.id) \
                .count()

            self.assertEqual(notifCount, 1)

    def testAcceptNotifications(self):
        
