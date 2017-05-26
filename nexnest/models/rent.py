from sqlalchemy import event

from datetime import datetime as dt

from nexnest.application import db

from nexnest.models.base import Base


class Rent(Base):
    __tablename__ = 'rents'
    id = db.Column(db.Integer, primary_key=True)
    house_id = db.Column(db.Integer, db.ForeignKey('houses.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    date_due = db.Column(db.Date())
    date_created = db.Column(db.DateTime)
    date_modified = db.Column(db.DateTime)

    def __init__(
            self,
            house,
            user,
            dateDue,
    ):

        self.house = house
        self.user = user
        self.date_due = dateDue

        # Default Values
        now = dt.now().isoformat()  # Current Time to Insert into Datamodels
        self.date_created = now
        self.date_modified = now

    def __repr__(self):
        return '<Rent ~ House %r | User %r>' % (self.house, self.user)


def update_date_modified(mapper, connection, target):
    # 'target' is the inserted object
    target.date_modified = dt.now().isoformat()  # Update Date Modified


event.listen(Rent, 'before_update', update_date_modified)
