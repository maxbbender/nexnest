from nexnest.application import db

from .message import Message

from .base import Base

from sqlalchemy import event


# class PostReport(Base):
class TourMessage(Message):
    __tablename__ = 'tour_messages'
    tour_id = db.Column(db.Integer,
                        db.ForeignKey('tours.id'),
                        primary_key=True)
    message_id = db.Column(db.Integer,
                           db.ForeignKey('messages.id'),
                           primary_key=True)

    __mapper_args__ = {
        'polymorphic_identity': 'tour',
    }

    def __init__(
            self,
            tour,
            message,
            content,
            user
    ):
        super().__init__(
            content=content,
            user=user
        )

        self.tour_id = tour.id

    def __repr__(self):
        return '<TourMessage ~ Tour %r | Message %r>' % \
            (self.tour_id, self.message_id)
