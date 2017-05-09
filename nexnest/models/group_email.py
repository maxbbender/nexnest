from sqlalchemy import event

from datetime import datetime as dt

from nexnest.application import db

from nexnest.models.base import Base


class GroupEmail(Base):
    __tablename__ = 'group_emails'
    id = db.Column(db.Integer, primary_key=True)
    group_id = db.Column(db.Integer, db.ForeignKey('groups.id'))
    email = db.Column(db.Text)
    date_created = db.Column(db.DateTime)
    date_modified = db.Column(db.DateTime)

    def __init__(
            self,
            group,
            email
    ):
        self.group = group
        self.email = email

        # Default Values
        now = dt.now().isoformat()  # Current Time to Insert into Datamodels
        self.date_created = now
        self.date_modified = now

    def __repr__(self):
        return '<GroupEmail Group %r | Email %s>' % (self.group, self.email)


def update_date_modified(mapper, connection, target):
    # 'target' is the inserted object
    target.date_modified = dt.now().isoformat()  # Update Date Modified


event.listen(GroupEmail, 'before_update', update_date_modified)
