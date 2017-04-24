from nexnest.application import db, session

from nexnest.models.notification import Notification

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

    def genNotifications(self):
        for user in self.group.acceptedUsers:
            if user is not self.user:
                if user.notificationPreference.group_message_notification:

                    newNotification = Notification(target_user=user,
                                                   target_model_id=self.id,
                                                   notif_type='group_message')

                    session.add(newNotification)
                    session.commit()

                if user.notificationPreference.group_message_email:
                    user.sendEmail(emailType='message',
                                   message=self.content)

    def __repr__(self):
        return '<GroupMessage ~ Group %r | Message %r>' % \
            (self.group_id, self.message_id)
