from nexnest.application import app, session
from sqlalchemy import desc

from nexnest.models import *

import os

from pprint import pprint
from nexnest.utils.school import allSchoolsAsStrings

import googlemaps

# u = session.query(landlord.Landlord).filter_by(user_id=1).first()
# print(u)
# pprint(u.getInProgressMaintenanceJSON())

# u = session.query(maintenance.Maintenance).filter_by(id=1).first()
# print(u)
# pprint(u.serialize)

# u = session.query(listing.Listing).filter_by(id=1).first()
# print(u)
# pprint(u.house[0])
# service = build('books', 'v1', developerKey="AIzaSyACeJxqY35gOjqNTIukZb6A6Zh6jvQnY3w")

# gmaps = googlemaps.Client(key='AIzaSyACeJxqY35gOjqNTIukZb6A6Zh6jvQnY3w')

# origins = '45 South Clover Street, Poughkeepsie NY'
# destinations = 'Marist College, Poughkeepsie NY'

# response = gmaps.distance_matrix(origins=origins,
#     destinations=destinations,
#     units='imperial')

# print("Response")
# pprint(response)

# print(listing_school.ListingSchool.__table__)

print(allSchoolsAsStrings())
