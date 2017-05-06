import string
import random
from faker import Faker

fake = Faker()


def idGenerator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def randomTime():
    time = fake.time()
    time.minute = 0
    time.second = 0
    return time
