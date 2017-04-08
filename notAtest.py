from nexnest.application import app, session
from sqlalchemy import desc

from nexnest.models import *

import os

from pprint import pprint
from nexnest.utils.school import allSchoolsAsStrings
import googlemaps

allListings = session.query(listing.Listing).filter(listing.Listing.num_bedrooms == 3)

allListings = allListings.filter(listing.Listing.cats).first()

print(allListings)
