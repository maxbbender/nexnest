from nexnest import db

from .base import Base


class LandlordListing(Base):
    __tablename__ = 'landlord_listings'
    landlord_id = db.Column(db.Integer,
                            db.ForeignKey('landlords.user_id'),
                            primary_key=True)

    listing_id = db.Column(db.Integer,
                           db.ForeignKey('listings.id'),
                           primary_key=True)

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
