from nexnest.application import db

from .message import Message


# class PostReport(Base):
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
        