# pylint: skip-file
import unittest

from nexnest import db

from nexnest.data_gen.factories import ListingFactory

from .utils import dropAllRows


class TestListing(unittest.TestCase):

    def setUp(self):
        self.listing = ListingFactory()
        db.session.commit()

    def tearDown(self):
        dropAllRows()

    def testRepr(self):
        self.assertEqual(self, '<Listing %r | %s>' % (self.listing.id, self.listing.street))
