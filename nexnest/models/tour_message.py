from datetime import datetime as dt

from nexnest.application import db

from .base import Base

from sqlalchemy import event


# class PostReport(Base):
class TourMessage(Base):
    __tablename__ = 'tour_messages'
    tour_id = db.Column(db.Integer,
                        db.ForeignKey('tours.id'),
                        primary_key=True)
    message_id = db.Column(db.Integer,
                           db.ForeignKey('messages.id'),
                           primary_key=True)
    date_created = db.Column(db.DateTime)
    date_modified = db.Column(db.DateTime)

    def __init__(
            self,
            tour,
            message
    ):
        self.tour = tour
        self.message = message

        # Default Values
        now = dt.now().isoformat()  # Current Time to Insert into Datamodels
        self.date_created = now
        self.date_modified = now

    def __repr__(self):
        return '<TourMessage ~ Tour %r | Message %r>' % \
            (self.tour_id, self.message_id)


def update_date_modified(mapper, connection, target):
    # 'target' is the inserted object
    target.date_modified = dt.now().isoformat()  # Update Date Modified


event.listen(TourMessage, 'before_update', update_date_modified)
