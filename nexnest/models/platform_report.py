from nexnest.application import db

from .report import Report


# class PostReport(Base):
class PlatformReport(Report):
    __tablename__ = 'platform_reports'
    id = db.Column(db.Integer, db.ForeignKey('reports.id'), primary_key=True)
    url = db.Column(db.Text)
    page_name = db.Column(db.Text)

    def __init__(
            self,
            url,
            page_name
    ):
        self.url = url
        self.page_name = page_name

    def __repr__(self):
        return '<Platform Report %r>' % self.id
