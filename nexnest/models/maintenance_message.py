from nexnest.application import db, session

from nexnest.models.notification import Notification
from nexnest.models.message import Message


class MaintenanceMessage(Message):
    __tablename__ = 'maintenance_messages'
    message_id = db.Column(db.Integer,
                           db.ForeignKey('messages.id'),
                           primary_key=True)
    maintenance_id = db.Column(db.Integer,
                               db.ForeignKey('maintenances.id'),
                               primary_key=True)

    __mapper_args__ = {
        'polymorphic_identity': 'maintenance',
    }

    def __init__(
            self,
            maintenance,
            content,
            user
    ):
        super().__init__(
            content=content,
            user=user
        )

        self.maintenance_id = maintenance.id

    def genNotifications(self):
        for user in self.maintenance.house.tenants:
            if user is not self.user:

                if user.notificationPreference.maintenance_message_notification:
                    newNotif = Notification(notif_type='maintenance_message',
                                            target_user=user,
                                            target_model_id=self.id)

                    session.add(newNotif)
                    session.commit()

                if user.notificationPreference.maintenance_message_email:
                    user.sendEmail(emailType='message',
                                   message=self.content)

        for landlord in self.maintenance.house.listing.landLordsAsUsers():
            if landlord.notificationPreference.maintenance_message_notification:
                newNotif = Notification(notif_type='maintenance_message',
                                        target_user=landlord,
                                        target_model_id=self.id)

                session.add(newNotif)
                session.commit()

            if landlord.notificationPreference.maintenance_message_email:
                user.sendEmail(emailType='message',
                               message=self.content)

    def __repr__(self):
        return '<MaintenanceMessage ~ Message %r | Maintenance %r>' % \
            (self.message_id, self.maintenance_id)
