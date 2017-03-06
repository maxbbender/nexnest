import unittest

from nexnest.application import session

from nexnest.data_gen.factories import GroupUserFactory, NotificationFactory
from nexnest.models.group_user import GroupUser
from nexnest.models.notification import Notification


class GroupUserTest(unittest.TestCase):

    def setUp(self):
        self.gu = GroupUserFactory()

        session.add(self.gu)
        session.commit()

    def tearDown(self):
        session.delete(self.gu)
        session.commit()
