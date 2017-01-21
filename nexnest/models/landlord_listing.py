from nexnest.application import db

from .base import Base

from sqlalchemy.orm import relationship


class LandlordListing(Base):
    __tablename__ = 'landlord_listings'
    landlord_id = db.Column(db.Integer,
                            db.ForeignKey('landlords.user_id'),
                            primary_key=True)

    listing_id = db.Column(db.Integer,
                           db.ForeignKey('listings.id'),
                           primary_key=True)
    landlord = relationship('Landlord', back_populates='listings')
    listing = relationship('Listing', back_populates='landlords')

    def __init__(
            self,
            landlord,
            listing
    ):
        self.landlord = landlord
        self.listing = listing

        self.landlord_id = landlord.user_id
        self.listing_id = listing.id

    def __repr__(self):
        return '<LandlordListing ~ Landlord %r | Listing %r>' % \
            (self.landlord_id, self.listing_id)
