from datetime import datetime as dt

from nexnest.application import db, session
from nexnest.models.notification import Notification

from .base import Base


class GroupListingFavorite(Base):
    __tablename__ = 'group_listing_favorites'
    id = db.Column(db.Integer, primary_key=True)
    group_id = db.Column(db.Integer, db.ForeignKey('groups.id'))
    listing_id = db.Column(db.Integer, db.ForeignKey('listings.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    show = db.Column(db.Boolean)
    date_created = db.Column(db.DateTime)

    def __init__(
            self,
            group,
            listing,
            user
    ):
        self.group_id = group.id
        self.listing_id = listing.id
        self.user_id = user.id
        self.show = True

        # Default Values
        now = dt.now().isoformat()  # Current Time to Insert into Datamodels
        self.date_created = now

    def __repr__(self):
        return '<GroupListingFavorite ~ Group %r | Listing %r>' % (self.group_id, self.listing_id)

    def genNotifications(self):
        for user in self.group.acceptedUsers:
            if user is not self.user:
                newNotf = Notification(notif_type='group_listing_favorite',
                                       target_model_id=self.id,
                                       target_user=user)
                session.add(newNotf)
                session.commit()
