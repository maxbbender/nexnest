from nexnest.application import db

from .base import Base


# class PostReport(Base):
class ReportGroup(Base):
    __tablename__ = 'report_groups'
    report_id = db.Column(db.Integer,
                          db.ForeignKey('reports.id'),
                          primary_key=True)
    group_id = db.Column(db.Integer,
                         db.ForeignKey('groups.id'),
                         primary_key=True)

    def __init__(
            self,
            report,
            group
    ):

        self.report = report
        self.group = group

    def __repr__(self):
        return '<ReportGroup ~ Report %r | Group %r>' % \
            (self.report_id, self.group_id)
