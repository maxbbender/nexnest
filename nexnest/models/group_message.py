from nexnest.application import db

from .message import Message


# class PostReport(Base):
class GroupMessage(Message):
    __tablename__ = 'group_messages'
    group_id = db.Column(db.Integer,
                         db.ForeignKey('groups.id'),
                         primary_key=True)
    message_id = db.Column(db.Integer,
                           db.ForeignKey('messages.id'),
                           primary_key=True)

    __mapper_args__ = {
        'polymorphic_identity': 'group',
    }

    def __init__(
            self,
            group,
            message
    ):
        self.group_id = group.id
        self.message_id = message.id

    def __repr__(self):
        return '<GroupMessage ~ Group %r | Message %r>' % \
            (self.group_id, self.message_id)
