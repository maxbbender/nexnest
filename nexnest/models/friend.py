from nexnest.application import db

from .base import Base

# class PostReport(Base):


class Friend(Base):
    __tablename__ = 'friends'
    source_user_id = db.Column(db.Integer,
                               db.ForeignKey('users.id'),
                               primary_key=True)
    target_user_id = db.Column(db.Integer,
                               db.ForeignKey('users.id'),
                               primary_key=True)
    accepted = db.Column(db.Boolean)

    def __init__(
            self,
            source_user,
            target_user
    ):

        self.source_user = source_user
        self.target_user = target_user
        self.accepted = False

    def __repr__(self):
        return '<Friend ~ Source User %r | Target User %r>' % \
            (self.source_user_id, self.target_user_id)
