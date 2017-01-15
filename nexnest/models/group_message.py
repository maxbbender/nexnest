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
            content,
            user,

    ):
        super().__init__(
            content=content,
            user=user
        )

        self.group_id = group.id

    def __repr__(self):
        return '<GroupMessage ~ Group %r | Message %r>' % \
            (self.group_id, self.message_id)
