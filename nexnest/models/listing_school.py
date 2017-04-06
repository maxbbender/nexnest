from sqlalchemy.orm import relationship

from nexnest.application import db

from nexnest.models.base import Base


class ListingSchool(Base):
    __tablename__ = 'listing_schools'
    listing_id = db.Column(db.Integer,
                           db.ForeignKey('listings.id'),
                           primary_key=True)

    school_id = db.Column(db.Integer,
                          db.ForeignKey('schools.id'),
                          primary_key=True)

    school = relationship('School', back_populates='listings')
    listing = relationship('Listing', back_populates='schools')

    def __init__(
            self,
            listing,
            school
    ):
        self.listing = listing
        self.school = school

    def __repr__(self):
        return '<School %r | Listing %r>' % (self.school, self.listing)
