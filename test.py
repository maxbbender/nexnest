from nexnest.application import app, session
from sqlalchemy import desc

from nexnest.models import *

import os


u = session.query(message.Message).filter_by(id=1).first()
print(u)
print(u.brief)

