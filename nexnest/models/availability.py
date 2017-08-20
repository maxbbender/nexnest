from nexnest import db

from nexnest.models.base import Base


class Availability(Base):
    __tablename__ = 'availability'
    landlord_id = db.Column(db.Integer, db.ForeignKey('landlords.user_id'), primary_key=True)
    time = db.Column(db.Time(), primary_key=True)
    day = db.Column(db.Integer, primary_key=True)

    def __init__(
            self,
            landlord,
            time,
            day
    ):

        self.landlord = landlord
        self.time = time
        self.day = day

    def __repr__(self):
        return '<Availability Landlord %r | Time %r>' % (self.landlord, self.time)

    @property
    def serialize(self):
        return {
            'time': self.time.strftime('%I:%M%p').lstrip("0").replace(" 0", " "),
            'day': self.day
        }
