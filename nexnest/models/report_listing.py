from nexnest import db

from nexnest.models.report import Report


class ReportListing(Report):
    __tablename__ = 'report_listings'
    report_id = db.Column(db.Integer,
                          db.ForeignKey('reports.id'),
                          primary_key=True)
    listing_id = db.Column(db.Integer,
                           db.ForeignKey('listings.id'),
                           primary_key=True)

    __mapper_args__ = {
        'polymorphic_identity': 'listing',
    }

    def __init__(
            self,
            title,
            content,
            listing,
            user,
            sourceURL=None,
    ):

        super().__init__(
            title=title,
            content=content,
            user=user,
            sourceURL=sourceURL
        )

        self.listing = listing

    def __repr__(self):
        return '<ReportListing ~ Report %r | Listing %r>' % \
            (self.report_id, self.listing_id)
