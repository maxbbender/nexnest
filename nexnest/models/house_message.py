from nexnest.application import db

from .message import Message


# class PostReport(Base):
class HouseMessage(Message):
    __tablename__ = 'house_messages'
    house_id = db.Column(db.Integer,
                         db.ForeignKey('houses.id'),
                         primary_key=True)
    message_id = db.Column(db.Integer,
                           db.ForeignKey('messages.id'),
                           primary_key=True)

    __mapper_args__ = {
        'polymorphic_identity': 'house',
    }

    def __init__(
            self,
            house,
            content,
            user,

    ):
        super().__init__(
            content=content,
            user=user
        )

        self.house_id = house.id

    def __repr__(self):
        return '<HouseMessage ~ House %r | Message %r>' % \
            (self.house_id, self.message_id)
