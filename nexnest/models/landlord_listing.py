from nexnest import db

from .base import Base


class LandlordListing(Base):
    __tablename__ = 'landlord_listings'
    landlord_id = db.Column(db.Integer,
                            primary_key=True,
                            db.ForeignKey('landlords.user_id'))
    listing_id = db.Column(db.Integer,
                           primary_key=True,
                           db.ForeignKey('listings.id'))

    def __init__(
            self,
            landlord,
            listing
    ):
        self.landlord = landlord
        self.listing = listing

    def __repr__(self):
        return '<LandlordListing ~ Landlord %r | Listing %r>' % \
            (self.landlord_id, self.listing_id)
