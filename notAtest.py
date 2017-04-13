from nexnest.application import app, session
from sqlalchemy import desc, or_

from nexnest.models import *

from nexnest import logger

import os
import re
import datetime

from pprint import pprint
from nexnest.utils.school import allSchoolsAsStrings
import googlemaps

Listing = listing.Listing
ListingSchool = listing_school.ListingSchool
School = school.School


# json = request.get_json(force=True)
# postedJSON = {
#     'bedrooms': 3,  # 1-4 (if at 4 it means 4+)
#     'distanceToCampus': 1,  # In miles
#     'includes': [  # If any of these are here this means that they are check, if not they are not checked. If they are check the listing HAS to have them. if not don't add to filter
#         # 'furnished',
#         'dishwasher',
#         'laundry',
#         # 'internet',
#         'cable',
#         'snowRemoval',
#         'garbageRemoval'
#     ],
#     'listingTypes': [  # Only show if element of list, don't show if not element
#         'house',
#         'apartment',
#         'complex'
#     ],
#     'school': 'Marist',  # This will be switched to school
#     'minPrice': 1000,
#     'maxPrice': 3000,
#     'pets': [  # Same as includes
#         'dogs',
#         # 'cats'
#     ],
#     'sortBy': None,  # priceLowToHigh|priceHighToLow|mostRecent|distanceToCampus
#     'term': '2017-2018 School Year'  # YYYY-YYYY [School Year|Summer]

# }
# # Required Fields : `bedrooms` | `minPrice` | `maxPrice` | `priceTerm` | `school`
# allListings = None

# # Bedroom Checks:
# if 'bedrooms' in postedJSON:
#     if postedJSON['bedrooms'] < 4:
#         allListings = session.query(Listing).filter(Listing.num_bedrooms == postedJSON['bedrooms'])
#     else:
#         allListings = session.query(Listing).filter(Listing.num_bedrooms >= 4)
# else:
#     logger.error("Bedrooms not found in listing search query")

# logger.debug("Bedrooms allListings %r" % allListings.all())

# # Price Checks
# if 'minPrice' in postedJSON and 'maxPrice' in postedJSON:
#     allListings = allListings.filter(Listing.price_per_month >= postedJSON['minPrice'], Listing.price_per_month <= postedJSON['maxPrice'])
# else:
#     logger.error('Minimum or Maximum price not found in listing search query')

# logger.debug("Price allListings %r" % allListings.all())

# # Term Checks
# if 'term' in postedJSON:
#     schoolYearPattern = re.compile(r"(\d{4}-\d{4})")
#     match = schoolYearPattern.match(postedJSON['term'])
#     if match:
#         allListings = allListings.filter(Listing.time_period_date_range == match.group(1),
#                                          or_(Listing.time_period == 'school',
#                                              Listing.time_period == 'year'))
#     else:
#         summerPattern = re.compile(r"(\d{4}) Summer")
#         match = summerPattern.match(postedJSON['term'])

#         if match:
#             allListings = allListings.filter(Listing.time_period_date_range == match.group(1),
#                                              Listing.time_period == 'summer')
#         else:
#             logger.error("term input is invalid and does not match any patterns defined. postedJSON['term'] : %s" % postedJSON['term'])
# else:
#     logger.error("Term not found in listing search query")

# logger.debug("Term allListings %r" % allListings.all())

# # School
# if 'school' in postedJSON:
#     school = session.query(School).filter_by(name=postedJSON['school']).first()

#     if school is not None:
#         if 'distanceToCampus' in postedJSON:
#             allListings = allListings.join(ListingSchool).filter(ListingSchool.school_id == school.id, int(postedJSON['distanceToCampus']) <=ListingSchool.driving_miles)
#         else:
#             allListings = allListings.join(ListingSchool).filter(ListingSchool.school_id == school.id)
#     else:
#         logger.error("Could not find school to apply to search filter. postedJSON['school'] : %s" % postedJSON['school'])
# else:
#     logger.error("School not found in listing search query")

# logger.debug("School allListings %r" % allListings.all())

# # Pets
# if 'pets' in postedJSON:
#     petList = postedJSON['pets']

#     if 'dogs' in petList:
#         allListings = allListings.filter(Listing.dogs == True)

#     if 'cats' in petList:
#         allListings = allListings.filter(Listing.cats == True)

# # Includes
# if 'includes' in postedJSON:
#     includeList = postedJSON['includes']

#     if 'furnished' in includeList:
#         allListings = allListings.filter(Listing.furnished == True)

#     if 'dishwasher' in includeList:
#         allListings = allListings.filter(Listing.dishwasher == True)

#     if 'laundry' in includeList:
#         allListings = allListings.filter(Listing.washer == True, Listing.dryer == True)

#     if 'internet' in includeList:
#         allListings = allListings.filter(Listing.internet == True)

#     if 'cable' in includeList:
#         allListings = allListings.filter(Listing.cable == True)

#     if 'snowRemoval' in includeList:
#         allListings = allListings.filter(Listing.snow_plowing == True)

#     if 'garbageRemoval' in includeList:
#         allListings = allListings.filter(Listing.garbage_service == True)

# # Listing Types
# if 'listingTypes' in postedJSON:
#     typeList = postedJSON['listingTypes']

#     if 'house' in typeList and 'apartment' in typeList and 'complex' in typeList:
#         allListings = allListings.filter(or_(Listing.property_type == 'house',
#                                              Listing.property_type == 'apartment',
#                                              Listing.property_type == 'complex',
#                                              ))
#     elif 'house' in typeList and 'apartment' in typeList:
#         allListings = allListings.filter(or_(Listing.property_type == 'house',
#                                              Listing.property_type == 'apartment'
#                                              ))
#     elif 'house' in typeList and 'complex' in typeList:
#         allListings = allListings.filter(or_(Listing.property_type == 'house',
#                                              Listing.property_type == 'complex'
#                                              ))
#     elif 'house' in typeList:
#         allListings = allListings.filter(Listing.property_type == 'house')

#     elif 'apartment' in typeList and 'complex' in typeList:
#         allListings = allListings.filter(or_(Listing.property_type == 'apartment',
#                                              Listing.property_type == 'complex'
#                                              ))
#     elif 'apartment' in typeList:
#         allListings = allListings.filter(Listing.property_type == 'apartment')

#     elif 'complex' in typeList:
#         allListings = allListings.filter(Listing.property_type == 'complex')
#     else:
#         logger.error("No Listing Types were defined to search for")


# print(allListings.all())
