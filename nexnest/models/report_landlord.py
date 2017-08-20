from nexnest import db

from nexnest.models.report import Report


class ReportLandlord(Report):
    __tablename__ = 'report_landlords'
    report_id = db.Column(db.Integer,
                          db.ForeignKey('reports.id'),
                          primary_key=True)
    landlord_id = db.Column(db.Integer,
                            db.ForeignKey('landlords.user_id'),
                            primary_key=True)

    __mapper_args__ = {
        'polymorphic_identity': 'landlord',
    }

    def __init__(
            self,
            title,
            content,
            landlord,
            user,
            sourceURL=None,
    ):

        super().__init__(
            title=title,
            content=content,
            user=user,
            sourceURL=sourceURL
        )

        self.landlord = landlord

    def __repr__(self):
        return '<ReportLandlord ~ Report %r | Landlord %r>' % \
            (self.report_id, self.landlord_id)
