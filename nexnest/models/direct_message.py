from nexnest.application import db

from nexnest.models.message import Message


class DirectMessage(Message):
    __tablename__ = 'direct_messages'
    target_user_id = db.Column(db.Integer,
                               db.ForeignKey('users.id'),
                               primary_key=True)
    message_id = db.Column(db.Integer,
                           db.ForeignKey('messages.id'),
                           primary_key=True)

    __mapper_args__ = {
        'polymorphic_identity': 'direct',
    }

    def __init__(
            self,
            source_user,
            target_user,
            content
    ):
        super().__init__(
            content=content,
            user=source_user
        )

        self.target_user_id = target_user.id

    def __repr__(self):
        return '<DirectMessage ~ Source %r | Target %r | Message %r>' % \
            (self.user_id, self.target_user_id, self.message_id)
