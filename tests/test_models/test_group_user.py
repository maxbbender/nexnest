import unittest

from nexnest.application import session

from nexnest.data_gen.factories import GroupUserFactory, NotificationFactory, UserFactory, GroupFactory

from nexnest.models.group_user import GroupUser
from nexnest.models.notification import Notification
from nexnest.models.user import User
from nexnest.models.group import Group

from .utils import dropAllRows


class TestGroupUser(unittest.TestCase):

    def setUp(self):
        self.leader = UserFactory()
        self.user = UserFactory()

        session.commit()

        self.group = GroupFactory(leader=self.leader)

        session.commit()

        self.gu = GroupUserFactory(group=self.group, user=self.user)

        session.add(self.gu)
        session.commit()

    def tearDown(self):
        dropAllRows()

    def testInitialGroupUser(self):
        groupUserCount = session.query(GroupUser).filter_by(user_id=self.leader.id, group_id=self.group.id).count()

        self.assertEqual(groupUserCount, 1)

    def testNotifications(self):
        notif = session.query(Notification) \
            .filter_by(notif_type='group_user',
                       target_model_id=self.gu.group.id,
                       target_user_id=self.gu.user.id) \
            .count()

        self.assertEqual(notif, 1)

    def userLeaveGroupNotifications(self):
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
