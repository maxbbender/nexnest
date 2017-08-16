from nexnest.application import db, session

from nexnest.models.message import Message
from nexnest.models.notification import Notification


class HouseMessage(Message):
    __tablename__ = 'house_messages'
    house_id = db.Column(db.Integer,
                         db.ForeignKey('houses.id'),
                         primary_key=True)
    message_id = db.Column(db.Integer,
                           db.ForeignKey('messages.id'),
                           primary_key=True)

    __mapper_args__ = {
        'polymorphic_identity': 'house',
    }

    def __init__(
            self,
            house,
            content,
            user,

    ):
        super().__init__(
            content=content,
            user=user
        )

        self.house_id = house.id

    def __repr__(self):
        return '<HouseMessage ~ House %r | Message %r>' % \
            (self.house_id, self.message_id)

    def genNotifications(self):
        # If the landlords sends the message
        if self.user in self.house.listing.landLordsAsUsers():
            for user in self.house.tenants:
                if user.notificationPreference.house_message_notification:
                    newNotification = Notification(target_user=user,
                                                   target_model_id=self.id,
                                                   notif_type='house_message')

                    session.add(newNotification)
                    session.commit()

                if user.notificationPreference.house_message_email:
                    user.sendEmail(emailType='houseMessage',
                                   message=self.genEmailContent(user))
        else:
            for user in self.house.tenants:
                if user is not self.user:
                    if user.notificationPreference.house_message_notification:
                        newNotification = Notification(target_user=user,
                                                       target_model_id=self.id,
                                                       notif_type='house_message')

                        session.add(newNotification)
                        session.commit()

                    if user.notificationPreference.house_message_email:
                        user.sendEmail(emailType='houseMessage',
                                       message=self.genEmailContent(user))

            for landlord in self.house.listing.landLordsAsUsers():
                if landlord.notificationPreference.house_message_notification:
                    newNotification = Notification(target_user=landlord,
                                                   target_model_id=self.id,
                                                   notif_type='house_message')

                    session.add(newNotification)
                    session.commit()

                    if landlord.notificationPreference.house_message_email:
                        landlord.sendEmail(emailType='houseMessage',
                                           message=self.genEmailContent(user))

    def genEmailContent(self, user):
        return """
        <div class="row">
            <div class="col-xs-1"></div>
            <div class="col-xs-10">
                <span>Hi %s,</span>
                <br><br>
                <span>
                    You have recieved a message in your house at %s!
                    <br>
                    <a href="https://nexnest.com/house/view/%d">Click  here</a> to see the message and stay connected. Don't leave them hanging!
                </span>
                <br><br>
            </div>
        </div>
        """ % (
            user.name,
            self.house.listing.briefStreet,
            self.house_id
        )
