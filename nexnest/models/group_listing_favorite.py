from datetime import datetime as dt

from nexnest import db
from nexnest.models.notification import Notification

from .base import Base

session = db.session


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
                if user.notificationPreference.group_listing_favorite_notification:
                    newNotf = Notification(notif_type='group_listing_favorite',
                                           target_model_id=self.id,
                                           target_user=user)
                    session.add(newNotf)
                    session.commit()

                if user.notificationPreference.group_listing_favorite_email:
                    user.sendEmail(emailType='groupListingFavorite',
                                   message=self.genEmailContent(user))

    def genEmailContent(self, user):
        return """
        <div class="row">
            <div class="col-xs-1"></div>
            <div class="col-xs-10">
                <span>Hi  %s ,</span>
                <br><br>
                <span>
                    One of your group members has favorited a new house in %s and wants you to check it out! <a href="https://nexnest.com/group/view/%d">Click here</a> to view your group’s favorites.
                    <br><br>
                    Don’t just wing it!
                </span>
                <br><br>
            </div>
        </div>
        """ % (
            user.fname,
            self.group.name,
            self.group.id
        )
