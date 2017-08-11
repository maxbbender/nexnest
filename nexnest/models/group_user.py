from nexnest.application import db, session
from nexnest.models.notification import Notification
from sqlalchemy.orm import relationship

from .base import Base


class GroupUser(Base):
    __tablename__ = 'group_users'
    id = db.Column(db.Integer,
                   primary_key=True)
    group_id = db.Column(db.Integer,
                         db.ForeignKey('groups.id'))
    user_id = db.Column(db.Integer,
                        db.ForeignKey('users.id'))

    # This is for if they have accepted to be a part of the group
    accepted = db.Column(db.Boolean)

    # A user might be invited to multiple groups, but he/she can only
    # be a part of one group at a time. On joining a group all other
    # records will have show set to False. However if a user is a part
    # of a group, then recieves a different group invite, show will be
    # True, so we know to display the notification
    show = db.Column(db.Boolean)

    group = relationship("Group", back_populates="users")
    user = relationship("User", back_populates='groups')

    def __init__(
            self,
            group,
            user
    ):
        self.group_id = group.id
        self.user_id = user.id
        self.group = group
        self.user = user

        self.accepted = False
        self.show = True

        # We create a notification for the target user.
        notif = Notification(target_user=user,
                             target_model_id=group.id,
                             notif_type='group_user')

        session.add(notif)
        session.commit()

    def __repr__(self):
        return '<GroupUser ~ Group %r | User %r>' % \
            (self.group_id, self.user_id)
