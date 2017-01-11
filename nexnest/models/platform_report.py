from nexnest.application import db

from .base import Base


# class PostReport(Base):
class PlatformReport(Base):
    __tablename__ = 'platform_reports'
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.Text)
    page_name = db.Column(db.Text)
    report_id = db.Column(db.Integer, db.ForeignKey('reports.id'))

    def __init__(
            self,
            url,
            page_name,
            report
    ):
        self.url = url
        self.page_name = page_name
        self.report = report

    def __repr__(self):
        return '<Platform Report %r>' % self.id
