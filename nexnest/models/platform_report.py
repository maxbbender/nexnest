from nexnest import db

from nexnest.models.report import Report
from nexnest.models.user import User


class PlatformReport(Report):
    __tablename__ = 'platform_reports'
    report_id = db.Column(db.Integer, db.ForeignKey('reports.id'), primary_key=True)

    __mapper_args__ = {
        'polymorphic_identity': 'platform',
    }

    def __init__(
            self,
            title,
            content,
            user=None,
            sourceURL=None,
    ):

        if user is None:
            user = User.query.first()

        super().__init__(
            title=title,
            content=content,
            user=user,
            sourceURL=sourceURL
        )

    def __repr__(self):
        return '<Platform Report %r>' % self.id
