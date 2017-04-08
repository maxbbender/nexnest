from nexnest.application import session

from nexnest.models.school import School

# Fredoia School
fredonia = School('SUNY at Fredonia',
                  '280 Central Ave',
                  'Fredonia',
                  'NY',
                  '14063',
                  '7166733111',
                  'http://home.fredonia.edu/')

marist = School('Marist',
                '3399 North Road',
                'Poughkeepsie',
                'NY',
                '12601',
                '8455753000',
                'http://www.marist.edu/')


session.add(fredonia)
session.add(marist)

session.commit()
