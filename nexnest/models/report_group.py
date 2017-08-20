from nexnest import db

from nexnest.models.report import Report


class ReportGroup(Report):
    __tablename__ = 'report_groups'
    report_id = db.Column(db.Integer,
                          db.ForeignKey('reports.id'),
                          primary_key=True)
    group_id = db.Column(db.Integer,
                         db.ForeignKey('groups.id'),
                         primary_key=True)

    __mapper_args__ = {
        'polymorphic_identity': 'group',
    }

    def __init__(
            self,
            title,
            content,
            group,
            user,
            sourceURL=None,
    ):

        super().__init__(
            title=title,
            content=content,
            user=user,
            sourceURL=sourceURL
        )

        self.group = group

    def __repr__(self):
        return '<ReportGroup ~ Report %r | Group %r>' % \
            (self.report_id, self.group_id)
