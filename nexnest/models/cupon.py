from datetime import datetime as dt

from sqlalchemy import event, UniqueConstraint

from nexnest.application import db, session
from nexnest.utils.misc import idGenerator

from .base import Base

from flask import flash


class Cupon(Base):
    __tablename__ = 'cupons'
    id = db.Column(db.Integer, primary_key=True)
    cupon_key = db.Column(db.Text)
    unlimited = db.Column(db.Boolean)
    uses = db.Column(db.Integer)
    percentage_off = db.Column(db.Integer)
    date_created = db.Column(db.DateTime)
    date_modified = db.Column(db.DateTime)

    __table_args__ = (
        UniqueConstraint('cupon_key'),
    )

    def __init__(
            self,
            percentage_off,
            cupon_key=None,
            unlimited=False,
            uses=0
    ):
        if cupon_key is None:
            self.cupon_key = self.genCuponKey()
        else:
            keyCount = session.query(Cupon).filter_by(cupon_key=cupon_key).count()

            if keyCount == 0:
                self.cupon_key = cupon_key
            else:
                newRandomKey = self.genCuponKey()
                self.cupon_key = newRandomKey
                flash('Cupon Key is already in use, generated a different key : %s' % self.cupon_key, 'warning')

        self.percentage_off = percentage_off
        self.unlimited = unlimited
        self.uses = uses

        # Default Values
        now = dt.now().isoformat()  # Current Time to Insert into Datamodels
        self.date_created = now
        self.date_modified = now

    def __repr__(self):
        return '<Cupon id:%d | key:%s>' % (self.id, self.cupon_key)

    @property
    def serialize(self):
        return {
            'cuponKey': self.cupon_key,
            'percentageOff': self.percentage_off,
            'uses': self.uses,
            'unlimited': self.unlimited
        }

    def genCuponKey(self):
        newRandomKey = idGenerator()

        keyCount = session.query(Cupon).filter_by(cupon_key=newRandomKey).count()

        while keyCount > 0:
            newRandomKey = idGenerator()

            keyCount = session.query(Cupon).filter_by(cupon_key=newRandomKey).count()

        return newRandomKey

    def cuponPrice(self, price):
        return price * 1 - (self.percentage_off / 100)


def update_date_modified(mapper, connection, target):
    # 'target' is the inserted object
    target.date_modified = dt.now().isoformat()  # Update Date Modified


event.listen(Cupon, 'before_update', update_date_modified)
