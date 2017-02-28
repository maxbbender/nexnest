from datetime import datetime as dt

from nexnest.application import db

from .base import Base

from sqlalchemy import event


# class PostReport(Base):
class SecurityDeposit(Base):
    __tablename__ = 'security_deposits'
    id = db.Column(db.Integer, primary_key=True)
    group_listing_id = db.Column(db.Integer, db.ForeignKey('group_listings.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    completed = db.Column(db.Boolean)
    date_created = db.Column(db.DateTime)
    date_modified = db.Column(db.DateTime)

    def __init__(
            self,
            groupListing,
            user
    ):

        self.group_listing_id = groupListing.id
        self.user_id = user.id
        self.completed = False

        # Default Values
        now = dt.now().isoformat()  # Current Time to Insert into Datamodels
        self.date_created = now
        self.date_modified = now

    def __repr__(self):
        return '<Security Deposit ~ GroupListing %r | User %r>' % (self.group_listing_id, self.user_id)


def update_date_modified(mapper, connection, target):
    # 'target' is the inserted object
    target.date_modified = dt.now().isoformat()  # Update Date Modified


event.listen(SecurityDeposit, 'before_update', update_date_modified)
