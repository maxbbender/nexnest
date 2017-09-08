import os
import sys

# Changing the directory and importing is hacky!
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)) + '/../')

from datetime import datetime
from nexnest import createApp, db
from nexnest.models.tour import Tour
from nexnest.models.tour_message import TourMessage
from nexnest.models.tour_time import TourTime
from sqlalchemy import and_

app = createApp(os.getenv('FLASK_CONFIG') or 'default')

now = datetime.now()

print('now: ', now)

dayStart = now.replace(hour=0, minute=0, second=0)
dayEnd = now.replace(hour=23, minute=59, second=59)

tmr = now + datetime.timedelta(days=1)
tmrStart = tmr.replace(hour=0, minute=0, second=0)
tmrEnd = tmr.replace(hour=23, minute=59, second=59)

print('dayStart', dayStart)
print('dayEnd', dayEnd)


def toursToday():
    with app.app_context():
        tourTimesToday = db.session.query(TourTime).filter_by(confirmed=True) \
            .filter(TourTime.date_time_requested > dayStart) \
            .filter(TourTime.date_time_requested < dayEnd) \
            .all()

        app.logger.debug('tourTimesToday %r' % tourTimesToday)
        return tourTimesToday


def toursTomorrow():
    with app.app_context():
        tourTimesTomorrow = db.session.query(TourTime).filter_by(confirmed=True) \
            .filter(TourTime.date_time_requested > tmrStart) \
            .filter(TourTime.date_time_requested < tmrEnd) \
            .all()

        app.logger.debug('tourTimesTomorrow %r' % tourTimesTomorrow)
        return tourTimesTomorrow


def toursTodayEmail():
    for tour in toursToday():

        # Each user in the group
        for user in tour.group.acceptedUsers:
            message = '''
            Hey %s,

            Don’t forget about your tour today! You have a scheduled tour at %s. We hope you enjoy the property. 

            Thanks for using nexnest.
            '''


toursToday()
