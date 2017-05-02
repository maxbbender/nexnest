from nexnest.application import db

from nexnest.models.report import Report


class PlatformReport(Report):
    __tablename__ = 'platform_reports'
    report_id = db.Column(db.Integer, primary_key=True, db.ForeignKey('reports.id'))

    __mapper_args__ = {
        'polymorphic_identity': 'platform',
    }

    def __init__(
            self,
            title,
            content,
            user,
            sourceURL=None,
    ):
        super().__init__(
            title=title,
            content=content,
            user=user,
            sourceURL=sourceURL
        )

    def __repr__(self):
        return '<Platform Report %r>' % self.id
