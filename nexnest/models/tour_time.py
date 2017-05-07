from sqlalchemy import event

from datetime import datetime as dt

from nexnest.application import db

from nexnest.models.base import Base


class TourTime(Base):
    __tablename__ = 'tour_times'
    tour_id = db.Column(db.Integer, db.ForeignKey('tours.id'), primary_key=True)
    date_time_requested = db.Column(db.DateTime(), primary_key=True)
    confirmed = db.Column(db.Boolean())
    date_created = db.Column(db.DateTime)
    date_modified = db.Column(db.DateTime)

    def __init__(
            self,
            tour,
            dateTimeRequested
    ):
        self.date_time_requested = dateTimeRequested
        self.tour = tour
        self.confirmed = False
        # Default Values
        now = dt.now().isoformat()  # Current Time to Insert into Datamodels
        self.date_created = now
        self.date_modified = now

    def __repr__(self):
        return '<TourTime %r | Time %r>' % (self.tour, self.date_time_requested)

    @property
    def serialize(self):
        return {
            'dateTimeRequested': self.humanISOComplaintString,
            'confirmed': self.confirmed
        }

    @property
    def humanISOComplaintString(self):
        return self.date_time_requested.strftime('%a, %b %-d %Y %I:%M%p')

    @property
    def humanString(self):
        return self.date_time_requested.strftime('%a %b %-d, %y at %I:%M%p')


def update_date_modified(mapper, connection, target):
    # 'target' is the inserted object
    target.date_modified = dt.now().isoformat()  # Update Date Modified


event.listen(TourTime, 'before_update', update_date_modified)
