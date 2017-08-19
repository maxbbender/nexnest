from nexnest import db

from .base import Base


# class PostReport(Base):
class SchoolUser(Base):
    __tablename__ = 'school_users'
    user_id = db.Column(db.Integer,
                        db.ForeignKey('users.id'),
                        primary_key=True)

    school_id = db.Column(db.Integer,
                          db.ForeignKey('schools.id'),
                          primary_key=True)

    def __init__(
            self,
            user,
            school,
    ):
        self.user_id = user.id
        self.school_id = school.id

    def __repr__(self):
        return '<SchoolUser ~ School %r | User %r>' % \
            (self.user_id, self.school_id)
