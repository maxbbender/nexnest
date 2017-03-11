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

    def genNotifications(self):
        # If the landlords sends the message
        if self.user in self.house.listing.landLordsAsUsers():
            for user in self.house.tenants:
                newNotification = Notification(target_user=user,
                                               target_model_id=self.id,
                                               notif_type='house_message')

                session.add(newNotification)
                session.commit()
        else:
            for user in self.house.tenants:
                if user is not self.user:
                    newNotification = Notification(target_user=user,
                                                   target_model_id=self.id,
                                                   notif_type='house_message')

                    session.add(newNotification)
                    session.commit()

            for landlord in self.house.listing.landLordsAsUsers():
                newNotification = Notification(target_user=landlord,
                                               target_model_id=self.id,
                                               notif_type='house_message')

                session.add(newNotification)
                session.commit()

    def __repr__(self):
        return '<HouseMessage ~ House %r | Message %r>' % \
            (self.house_id, self.message_id)
