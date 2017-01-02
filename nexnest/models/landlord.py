from .base import Base

from nexnest import db


class Landlord(Base):
    __tablename__ = 'landlords'
    user_id = db.Column(db.Integer,
                        primary_key=True,
                        db.ForeignKey('users.id'))
    online_pay = db.Column(db.Boolean)
    check_pay = db.Column(db.Boolean)
    street = db.Column(db.Text)
    city = db.Column(db.Text)
    state = db.Column(db.String(2))
    zip_code = db.Column(db.String(5))

    def __init__(self,
                 user,
                 online_pay,
                 check_pay,
                 street,
                 city,
                 state,
                 zip_code):
        self.user = user
        self.online_pay = online_pay
        self.check_pay = check_pay
        self.street = street
        self.city = city
        self.state = state
        self.zip_code = zip_code

    def __repr__(self):
    	return '<Landlord %r>' % user_id
