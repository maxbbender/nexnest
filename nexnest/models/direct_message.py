from nexnest import db
from nexnest.models.message import Message
from nexnest.models.notification import Notification

session = db.session


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

    @property
    def serialize(self):
        returnDict = super().serialize
        returnDict['targetUser'] = self.target_user.serialize
        return returnDict

    def genNotifications(self):
        print(self.target_user)
        print(self.target_user.notificationPreference.direct_message_notification)

        if self.target_user.notificationPreference.direct_message_notification:
            newNotification = Notification(target_user=self.target_user,
                                           target_model_id=self.user_id,
                                           notif_type='direct_message')

            session.add(newNotification)
            session.commit()

        if self.target_user.notificationPreference.direct_message_email:
            self.target_user.sendEmail(emailType='directMessage',
                                       message=self.genEmailContent(self.target_user))

    def genEmailContent(self, user):
        return """
        <div class="row">
            <div class="col-xs-1"></div>
            <div class="col-xs-10">
                <span>Hi %s,</span>
                <br><br>
                <span>
                    You have recieved a new direct message from %s.
                    <br>
                    <a href="https://nexnest.com/user/directMessages/%d">Click  here</a> to see the message and stay connected. Don't leave them hanging!
                </span>
                <br><br>
            </div>
        </div>
        """ % (
            user.name,
            self.user.name,
            self.target_user_id
        )
