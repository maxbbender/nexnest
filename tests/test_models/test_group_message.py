import unittest

from nexnest.application import session

from nexnest.data_gen.factories import GroupMessageFactory, UserFactory, GroupFactory, GroupUserFactory

from nexnest.models.notification import Notification
from nexnest.models.user import User
from nexnest.models.group import Group
from nexnest.models.group_user import GroupUser
from nexnest.models.group_message import GroupMessage
from nexnest.models.message import Message

from .utils import dropAllRows


class TestGroupMessage(unittest.TestCase):

    def setUp(self):
        self.leader = UserFactory()
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

        self.groupMessage = GroupMessageFactory(group=self.group,
                                                user=self.leader)

        session.add(self.groupMessage)
        session.commit()

        self.groupMessage.genNotifications()

    def tearDown(self):
        dropAllRows()
        # session.query(GroupMessage).delete()
        # session.commit()
        # session.query(Message).delete()
        # session.commit()
        # session.query(GroupUser).delete()
        # session.commit()
        # session.query(Group).delete()
        # session.commit()
        # session.query(Notification).delete()
        # session.commit()
        # session.query(User).delete()
        # session.commit()

    def testGroupMessageCreate(self):
        print("Trying to find all the notifications")
        notTests = session.query(Notification).filter_by(notif_type='group_message').all()

        print("All Notifications w/ notif_type=group_message %r" % notTests)

        print("Target Model ID we are looking for : %d" % self.groupMessage.id)

        for no in notTests:
            print("Target Model ID for %r is %d" % (no, no.target_model_id))

        notifCount = session.query(Notification)\
            .filter_by(notif_type='group_message',
                       target_model_id=self.groupMessage.id)\
            .count()

        print("notif count %d" % notifCount)

        self.assertEqual(notifCount, 4)
