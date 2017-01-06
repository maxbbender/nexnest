from datetime import datetime as dt

from nexnest.application import db

from .base import Base

from sqlalchemy import event


# class PostReport(Base):
class UserRole(Base):
    __tablename__ = 'user_roles'
    user_id = db.Column(db.Integer,
                        db.ForeignKey('users.id'),
                        primary_key=True)
    role_id = db.Column(db.Integer,
                        db.ForeignKey('roles.id'),
                        primary_key=True)
    date_created = db.Column(db.DateTime)
    date_modified = db.Column(db.DateTime)

    def __init__(
            self,
            user,
            role
    ):
        self.user = user
        self.role = role

        # Default Values
        now = dt.now().isoformat()  # Current Time to Insert into Datamodels
        self.date_created = now
        self.date_modified = now

    def __repr__(self):
        return '<UserRole ~ User %r | Role %r>' % (self.user_id, self.role_id)


def update_date_modified(mapper, connection, target):
    # 'target' is the inserted object
    target.date_modified = dt.now().isoformat()  # Update Date Modified


event.listen(UserRole, 'before_update', update_date_modified)
