from nexnest.application import db, session

from nexnest.models.message import Message
from nexnest.models.notification import Notification


class TourMessage(Message):
    __tablename__ = 'tour_messages'
    tour_id = db.Column(db.Integer,
                        db.ForeignKey('tours.id'),
                        primary_key=True)
    message_id = db.Column(db.Integer,
                           db.ForeignKey('messages.id'),
                           primary_key=True)

    __mapper_args__ = {
        'polymorphic_identity': 'tour',
    }

    def __init__(
            self,
            tour,
            content,
            user
    ):
        super().__init__(
            content=content,
            user=user
        )

        self.tour_id = tour.id

    def __repr__(self):
        return '<TourMessage ~ Tour %r | Message %r>' % \
            (self.tour_id, self.message_id)

    def genNotifications(self):
        for user in self.tour.group.acceptedUsers:
            if user is not self.user:
                if user.notificationPreference.tour_message_notification:
                    newNotif = Notification(notif_type='tour_message',
                                            target_user=user,
                                            target_model_id=self.id)
                    session.add(newNotif)
                    session.commit()

                if user.notificationPreference.tour_message_email:
                    user.sendEmail(emailType='tourMessage',
                                   message=self.genEmailContent(user))

        for user in self.tour.listing.landLordsAsUsers():
            if user is not self.user:
                if user.notificationPreference.tour_message_notification:
                    newNotif = Notification(notif_type='tour_message',
                                            target_user=user,
                                            target_model_id=self.id)
                    session.add(newNotif)
                    session.commit()

                if user.notificationPreference.tour_message_email:
                    user.sendEmail(emailType='tourMessage',
                                   message=self.genEmailContent(user))

    def genEmailContent(self, user):
        return """
        <div class="row">
            <div class="col-xs-1"></div>
            <div class="col-xs-10">
                <span>Hi %s,</span>
                <br><br>
                <span>
                    You have recieved a message in your tour request for %s.
                    <br>
                    <a href="https://nexnest.com/tour/view/%d">Click  here</a> to see the message and stay connected. Don't leave them hanging!
                </span>
                <br><br>
            </div>
        </div>
        """ % (
            user.name,
            self.tour.listing.briefStreet,
            self.tour_id
        )
