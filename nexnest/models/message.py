from datetime import datetime as dt

from sqlalchemy import event

from nexnest.application import db

from .base import Base


class Message(Base):
    __tablename__ = 'messages'
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    date_created = db.Column(db.DateTime)
    date_modified = db.Column(db.DateTime)
    type = db.Column(db.String(50))

    __mapper_args__ = {
        'polymorphic_identity': 'messages',
        'polymorphic_on': type
    }

    def __init__(
            self,
            content,
            user
    ):
        self.content = content
        self.user_id = user.id

        # Default Values
        now = dt.now().isoformat()  # Current Time to Insert into Datamodels
        self.date_created = now
        self.date_modified = now

    def __repr__(self):
        return '<Message %r>' % self.id

    @property
    def brief(self):
        return self.content[0:50] + "..."


def update_date_modified(mapper, connection, target):  # pylint: disable=unused-argument
    # 'target' is the inserted object
    target.date_modified = dt.now().isoformat()  # Update Date Modified


event.listen(Message, 'before_update', update_date_modified)
