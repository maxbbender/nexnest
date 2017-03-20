import unittest

from nexnest.application import session

from nexnest.data_gen.factories import UserFactory

from .utils import dropAllRows


class TestUser(unittest.TestCase):

    def setUp(self):
        self.user = UserFactory()
        session.commit()

    def tearDown(self):
        dropAllRows()

    def testShortSerialize(self):
        serializedDict = self.user.shortSerialize

        self.assertEqual(serializedDict['name'], self.user.name)
        self.assertEqual(serializedDict['id'], self.user.id)
