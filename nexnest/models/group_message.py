from nexnest import db

from nexnest.models.notification import Notification

from .message import Message


session = db.session


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
                    user.sendEmail(emailType='groupMessage',
                                   message=self.genEmailContent(user))

    def genEmailContent(self, user):
        return """
        <div class="row">
            <div class="col-xs-1"></div>
            <div class="col-xs-10">
                <span>Hi %s,</span>
                <br><br>
                <span>
                    You have recieved a new message in your group %s.
                    <br>
                    <a href="https://nexnest.com/group/view/%d">Click  here</a> to see the message and stay connected. Don't leave them hanging!
                </span>
                <br><br>
            </div>
        </div>
        """ % (
            user.name,
            self.group.name,
            self.group_id
        )
