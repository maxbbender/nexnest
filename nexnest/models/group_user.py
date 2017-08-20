from nexnest import db
from nexnest.models.notification import Notification
from sqlalchemy.orm import relationship

from .base import Base

session = db.session


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

    def __repr__(self):
        return '<GroupUser ~ Group %r | User %r>' % \
            (self.group_id, self.user_id)

    def genNotifications(self):
        # We create a notification for the target user.
        if self.user.notificationPreference.group_user_notification:
            notif = Notification(target_user=self.user,
                                 target_model_id=self.group_id,
                                 notif_type='group_user')

            session.add(notif)
            session.commit()

    def genCompletedNotifications(self):
        for user in self.group.acceptedUsers:
            if user is not self.user:

                if user.notificationPreference.group_user_completed_notification:
                    newNotif = Notification(notif_type='group_user_completed',
                                            target_model_id=self.id,
                                            target_user=user)
                    session.add(newNotif)
                    session.commit()

                if user.notificationPreference.group_user_completed_email:
                    user.sendEmail(emailType='groupUserCompleted',
                                   message=self.genCompletedEmailContent(user))

    def genCompletedEmailContent(self, user):
        return """
        <div class="row">
            <div class="col-xs-1"></div>
            <div class="col-xs-10">
                <span>Hi  %s ,</span>
                <br><br>
                <span>
                    A new birdie has joined your nest! %s has joined %s
                    <br><br>
                    Don’t just wing it! Chat, favorite and share listings with your housemates to find the perfect college rental for you and your friends.
                    <br><br>
                    <a href="https://nexnest.com/group/view/%d">Click here</a> to view the group or <a href="https://nexnest.com/index#search">start searching</a> for listings in your area
                </span>
                <br><br>
            </div>
        </div>
        """ % (
            user.fname,
            self.user.name,
            self.group.name,
            self.group.id
        )
