from sqlalchemy import event

from datetime import datetime as dt

from nexnest.application import db

from nexnest.models.base import Base


class Availability(Base):
    __tablename__ = 'XXXX'
    landlord_id = db.Column(db.Integer, db.ForeignKey('landlords.user_id'), primary_key=True)
    time = db.Column(db.Time())

    def __init__(
            self,
            landlord,
            time
    ):

        self.landlord = landlord
        self.time = time

    def __repr__(self):
        return '<Availability Landlord %r | Time %r>' % (self.landlord, self.time)
