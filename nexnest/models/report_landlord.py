from nexnest.application import db

from .base import Base


# class PostReport(Base):
class ReportLandlord(Base):
    __tablename__ = 'report_landlords'
    report_id = db.Column(db.Integer,
                          db.ForeignKey('reports.id'),
                          primary_key=True)
    landlord_id = db.Column(db.Integer,
                            db.ForeignKey('landlords.user_id'),
                            primary_key=True)

    def __init__(
            self,
            report,
            landlord
    ):
        self.report = report
        self.landlord = landlord

    def __repr__(self):
        return '<ReportLandlord ~ Report %r | Landlord %r>' % \
            (self.report_id, self.landlord_id)
