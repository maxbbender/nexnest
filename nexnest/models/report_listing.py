from nexnest.application import db

from .base import Base


# class PostReport(Base):
class ReportListing(Base):
    __tablename__ = 'report_listings'
    report_id = db.Column(db.Integer,
                          db.ForeignKey('reports.id'),
                          primary_key=True)
    listing_id = db.Column(db.Integer,
                           db.ForeignKey('listings.id'),
                           primary_key=True)

    def __init__(
            self,
            report,
            listing
    ):
        self.report = report
        self.listing = listing

    def __repr__(self):
        return '<ReportListing ~ Report %r | Listing %r>' % \
            (self.report_id, self.listing_id)
