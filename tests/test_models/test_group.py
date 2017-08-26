import unittest

from nexnest import db

from nexnest.data_gen.factories import GroupUserFactory, NotificationFactory, UserFactory, GroupFactory, GroupMessageFactory, ListingFactory, GroupListingFavoriteFactory

from nexnest.models.group_user import GroupUser
from nexnest.models.notification import Notification
from nexnest.models.user import User
from nexnest.models.group import Group
from nexnest.models.notification_preference import NotificationPreference

from .utils import dropAllRows

session = db.session


class TestGroup(unittest.TestCase):

    def setUp(self):
        self.leader = UserFactory()
        session.commit()

        newNotifPref = NotificationPreference(user=self.leader)
        session.add(newNotifPref)
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

    def tearDown(self):
        dropAllRows()

    def testGroupMessageNotifications(self):
        groupMessage = GroupMessageFactory(group=self.group,
                                           user=self.leader)

        session.add(groupMessage)
        session.commit()

        groupMessage.genNotifications()

        for user in self.group.acceptedUsers:
            if user is not self.leader:
                notifCount = session.query(Notification) \
                    .filter_by(notif_type='group_message',
                               target_model_id=groupMessage.id,
                               target_user_id=user.id) \
                    .count()

                self.assertEqual(notifCount, 1)

    def testInitialGroupUser(self):
        groupUserCount = session.query(GroupUser) \
            .filter_by(user_id=self.leader.id,
                       group_id=self.group.id) \
            .count()

        self.assertEqual(groupUserCount, 1)

    def testGroupUserInviteNotification(self):
        newUser = UserFactory()
        session.commit()

        newGU = GroupUserFactory(user=newUser, group=self.group)
        session.commit()

        # Now there should be a notification for the user saying
        # he/she was invited
        notif = session.query(Notification) \
            .filter_by(notif_type='group_user',
                       target_model_id=newGU.group.id,
                       target_user_id=newGU.user.id) \
            .count()

        self.assertEqual(notif, 1)

    def testUserLeaveGroupNotifications(self):
        newUser = UserFactory()
        session.commit()

        newGU = GroupUserFactory(group=self.group, user=newUser)
        newGU.accepted = True
        session.commit()

        # Now the user leaves the group
        newUser.leaveGroup(self.group)

        # Now there should be a notification for each of the group's
        # accepted users
        for user in self.group.acceptedUsers:
            notifCount = session.query(Notification) \
                .filter_by(notif_type='user_leave_group',
                           target_model_id=newGU.id,
                           target_user_id=user.id) \
                .count()

            self.assertEqual(notifCount, 1)

    def testGroupFavoriteNotifications(self):
        listing = ListingFactory()
        session.commit()
        newGLF = GroupListingFavoriteFactory(group=self.group,
                                             listing=listing,
                                             user=self.leader)

        session.commit()

        newGLF.genNotifications()

        # We should see 4 notifications for this group listing favorite
        for user in self.group.acceptedUsers:
            if user is not self.leader:
                notifCount = session.query(Notification) \
                    .filter_by(notif_type='group_listing_favorite',
                               target_model_id=newGLF.id,
                               target_user_id=user.id) \
                    .count()

                self.assertEqual(notifCount, 1)
