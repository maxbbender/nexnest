from nexnest import db

from nexnest.models.user import User
from nexnest.models.school import School

# Fredoia School
fredonia = School('SUNY at Fredonia',
                  '280 Central Ave',
                  'Fredonia',
                  'NY',
                  '14063',
                  '7166733111',
                  'http://home.fredonia.edu/',
                  42.4540921,
                  -79.3340398)

marist = School('Marist',
                '3399 North Road',
                'Poughkeepsie',
                'NY',
                '12601',
                '8455753000',
                'http://www.marist.edu/',
                41.7225603,
                -73.9324651)


db.session.add(fredonia)
db.session.add(marist)

db.session.commit()
