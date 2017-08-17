import string
import random
from faker import Faker

import datetime
import calendar

fake = Faker()


def idGenerator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def randomTime():
    time = fake.time()
    time.minute = 0
    time.second = 0
    return time


def add_months(sourcedate, months):
    month = sourcedate.month - 1 + months
    year = int(sourcedate.year + month / 12)
    month = month % 12 + 1
    day = min(sourcedate.day, calendar.monthrange(year, month)[1])
    return datetime.date(year, month, day)


def isWithin30Days(date):
    now = datetime.datetime.now()

    nowPlus30Days = now + datetime.timedelta(30)

    if date < nowPlus30Days.date() and date >= now.date():
        return True

    return False
