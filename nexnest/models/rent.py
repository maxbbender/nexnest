from sqlalchemy import event
from sqlalchemy.orm import relationship

from datetime import datetime as dt

from nexnest.application import db

from nexnest.models.base import Base


class Rent(Base):
    __tablename__ = 'rents'
    id = db.Column(db.Integer, primary_key=True)
    house_id = db.Column(db.Integer, db.ForeignKey('houses.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    date_due = db.Column(db.Date())
    completed = db.Column(db.Boolean)
    amount = db.Column(db.Integer)
    date_created = db.Column(db.DateTime)
    date_modified = db.Column(db.DateTime)
    transaction = relationship("RentTransaction", uselist=False, back_populates='rent')

    def __init__(
            self,
            house,
            user,
            dateDue,
            amount
    ):

        self.house = house
        self.user = user
        self.date_due = dateDue
        self.amount = amount

        # Default Values
        now = dt.now().isoformat()  # Current Time to Insert into Datamodels
        self.date_created = now
        self.date_modified = now

    def __repr__(self):
        return '<Rent ~ House %r | User %r>' % (self.house, self.user)

    def isEditableBy(self, user, toFlash=True):
        if user == self.user or user in self.house.listing.landLordsAsUsers():
            return True

        return False

    def isViewableBy(self, user, toFlash=True):
        return self.isEditableBy(user, toFlash)


def update_date_modified(mapper, connection, target):
    # 'target' is the inserted object
    target.date_modified = dt.now().isoformat()  # Update Date Modified


event.listen(Rent, 'before_update', update_date_modified)
