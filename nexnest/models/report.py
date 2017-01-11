from datetime import datetime as dt

from nexnest.application import db

from .base import Base

from sqlalchemy import event


class Report(Base):
    __tablename__ = 'reports'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text)
    content = db.Column(db.Text)
    date_created = db.Column(db.DateTime)
    date_modified = db.Column(db.DateTime)

    def __init__(
            self,
            title,
            content
    ):
        self.title = title
        self.content = content
        # Default Values
        now = dt.now().isoformat()  # Current Time to Insert into Datamodels
        self.date_created = now
        self.date_modified = now

    def __repr__(self):
        return '<Report %r>' % self.id


def update_date_modified(mapper, connection, target):
    # 'target' is the inserted object
    target.date_modified = dt.now().isoformat()  # Update Date Modified


event.listen(Report, 'before_update', update_date_modified)
