from datetime import datetime as dt

from nexnest import db

from .base import Base

from sqlalchemy import event


# class PostReport(Base):
class GroupUser(Base):
    __tablename__ = 'group_users'
    group_id = db.Column(db.Integer,
                         primary_key=True,
                         db.ForiegnKey('groups.id'))
    user_id = db.Column(db.Integer,
                        primary_key=True,
                        db.ForiegnKey('users.id'))

    def __init__(
            self,
            group,
            user
    ):
        self.group = group
        self.user = user

    def __repr__(self):
        return '<GroupUser ~ Group %r | User %r>' % \
            (self.group_id, self.user_id)
