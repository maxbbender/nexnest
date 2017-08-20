from nexnest import db
from nexnest.models.notification import Notification

from .message import Message

session = db.session


class GroupListingMessage(Message):
    __tablename__ = 'group_listing_messages'
    groupListingID = db.Column(db.Integer,
                               db.ForeignKey('group_listings.id'),
                               primary_key=True)
    messageID = db.Column(db.Integer,
                          db.ForeignKey('messages.id'),
                          primary_key=True)

    __mapper_args__ = {
        'polymorphic_identity': 'groupListing',
    }

    def __init__(
            self,
            groupListing,
            content,
            user,

    ):
        super().__init__(
            content=content,
            user=user
        )

        self.groupListingID = groupListing.id

    def __repr__(self):
        return '<GroupListingMessage ~ GroupListing %r | Message %r>' % (self.groupListingID, self.messageID)

    def genNotifications(self):
        # Did the message come from one of the landlords?
        if self.user in self.groupListing.listing.landLordsAsUsers():
            for user in self.groupListing.group.acceptedUser:
                newNotif = Notification(notif_type='group_listing_message',
                                        target_model_id=self.id,
                                        target_user=user)
                session.add(newNotif)
                session.commit()
        else:
            for user in self.groupListing.group.acceptedUsers:
                if user is not self.user:
                    newNotif = Notification(notif_type='group_listing_message',
                                            target_model_id=self.id,
                                            target_user=user)
                    session.add(newNotif)
                    session.commit()

            for user in self.groupListing.listing.landLordsAsUsers():
                newNotif = Notification(notif_type='group_listing_message',
                                        target_model_id=self.id,
                                        target_user=user)
                session.add(newNotif)
                session.commit()
