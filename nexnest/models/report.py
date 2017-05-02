from datetime import datetime as dt

from sqlalchemy import event

from nexnest.application import db

from .base import Base


class Report(Base):
    __tablename__ = 'reports'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text)
    content = db.Column(db.Text)
    source_url = db.Column(db.Text)
    type = db.Column(db.String(50))
    user_id = db.Column(db.Integer)
    date_created = db.Column(db.DateTime)
    date_modified = db.Column(db.DateTime)

    __mapper_args__ = {
        'polymorphic_identity': 'reports',
        'polymorphic_on': type
    }

    def __init__(
            self,
            title,
            content,
            user,
            sourceURL=None,
    ):
        self.title = title
        self.content = content
        self.source_url = sourceURL
        self.user = user
        # Default Values
        now = dt.now().isoformat()  # Current Time to Insert into Datamodels
        self.date_created = now
        self.date_modified = now

    def __repr__(self):
        return '<Report %r>' % self.id

    @property
    def sourceURL(self):
        return self.source_url


def update_date_modified(mapper, connection, target):  # pylint: disable=unused-argument
    # 'target' is the inserted object
    target.date_modified = dt.now().isoformat()  # Update Date Modified


event.listen(Report, 'before_update', update_date_modified)
