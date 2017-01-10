from datetime import datetime as dt

from nexnest.application import db

from .base import Base

from sqlalchemy import event


# class PostReport(Base):
class DirectMessage(Base):
    __tablename__ = 'direct_messages'
    source_user_id = db.Column(db.Integer,
                               db.ForeignKey('users.id'),
                               primary_key=True)
    target_user_id = db.Column(db.Integer,
                               db.ForeignKey('users.id'),
                               primary_key=True)
    message_id = db.Column(db.Integer,
                           db.ForeignKey('messages.id'),
                           primary_key=True)
    date_created = db.Column(db.DateTime)
    date_modified = db.Column(db.DateTime)

    def __init__(
            self,
            source_user,
            target_user,
            message
    ):

        self.source_user_id = source_user.id
        self.target_user_id = target_user.id
        self.message_id = message.id

        # Default Values
        now = dt.now().isoformat()  # Current Time to Insert into Datamodels
        self.date_created = now
        self.date_modified = now

    def __repr__(self):
        return '<DirectMessage ~ Source %r | Target %r | Message %r>' % \
            (self.source_user_id, self.target_user_id, self.message_id)


def update_date_modified(mapper, connection, target):
    # 'target' is the inserted object
    target.date_modified = dt.now().isoformat()  # Update Date Modified


event.listen(DirectMessage, 'before_update', update_date_modified)
