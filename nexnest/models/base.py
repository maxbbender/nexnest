from sqlalchemy.ext.declarative import declarative_base
from nexnest.application import session


def update(self, data):
    for key in data:
        if data[key] == "":
            data[key] = None

        setattr(self, key, data[key])

    return self


Base = declarative_base()

Base.update = update
Base.query = session.query_property()
