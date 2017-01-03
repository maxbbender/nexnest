from nexnest.application import db

from .base import Base


class GroupUser(Base):
    __tablename__ = 'group_users'
    group_id = db.Column(db.Integer,
                         db.ForeignKey('groups.id'),
                         primary_key=True)
    user_id = db.Column(db.Integer,
                        db.ForeignKey('users.id'),
                        primary_key=True)

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
