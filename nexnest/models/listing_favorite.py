from nexnest.application import db

from .base import Base


# class PostReport(Base):
class ListingFavorite(Base):
    __tablename__ = 'listing_favorites'
    listing_id = db.Column(db.Integer,
                           db.ForeignKey('listings.id'),
                           primary_key=True)

    user_id = db.Column(db.Integer,
                        db.ForeignKey('users.id'),
                        primary_key=True)

    def __init__(
            self,
            listing,
            user
    ):
        self.listing = listing
        self.user = user

    def __repr__(self):
        return '<ListingFavorite ~ Listing %r | User %r>' % \
            (self.listing_id, self.user_id)
