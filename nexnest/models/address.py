from .base import Base

from nexnest import db


class Address(Base):
    id = db.Column(db.Integer)
    street = db.Column(db.Text)
    city = db.Column(db.Text)
    state = db.Column(db.String(2))
    zip_code = db.Column(db.String(5))

    def __init__(self,
                 street,
                 city,
                 state,
                 zip_code):

        self.street = street
        self.city = city
        self.state = state
        self.zip_code = zip_code
