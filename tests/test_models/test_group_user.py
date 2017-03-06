import unittest

from nexnest.application import session

from nexnest.data_gen.factories import GroupUserFactory, NotificationFactory, UserFactory, GroupFactory

from nexnest.models.group_user import GroupUser
from nexnest.models.notification import Notification


class testGroupUser(unittest.TestCase):

    def setUp(self):
        self.leader = UserFactory()
        self.user = UserFactory()

        session.commit()

        self.group = GroupFactory(leader=self.user)

        session.commit()

        self.gu = GroupUserFactory(group=self.group, user=self.user)

        session.add(self.gu)
        session.commit()

    def tearDown(self):
        session.delete(self.gu)
        session.delete(self.leader)
        session.delete(self.user)
        session.delete(self.group)
        session.commit()

    def testNotification(self):
        notif = session.query(Notification) \
            .filter_by(notif_type='group_user',
                       target_model_id=self.gu.group.id,
                       target_user_id=self.gu.user.id) \
            .count()

        self.assertEqual(notif, 1)
