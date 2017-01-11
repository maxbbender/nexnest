from nexnest.application import session

from nexnest.models.school import School

# Fredoia School
fredonia = School('Fredonia',
                  '280 Central Ave',
                  'Fredonia',
                  'NY',
                  '14063',
                  '7166733111',
                  'http://home.fredonia.edu/')

# First check to see that school doesn't exist
count = session.query(School).filter_by(name='Fredonia').count()

if count == 0:
    session.add(fredonia)
    session.commit()
