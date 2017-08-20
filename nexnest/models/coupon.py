from datetime import datetime as dt

from sqlalchemy import event, UniqueConstraint
from sqlalchemy.orm import relationship

from nexnest import db
from nexnest.utils.misc import idGenerator

from .base import Base

from flask import flash

session = db.session


class Coupon(Base):
    __tablename__ = 'coupons'
    id = db.Column(db.Integer, primary_key=True)
    coupon_key = db.Column(db.Text)
    unlimited = db.Column(db.Boolean)
    uses = db.Column(db.Integer)
    percentage_off = db.Column(db.Integer)
    date_created = db.Column(db.DateTime)
    date_modified = db.Column(db.DateTime)

    listingTransaction = relationship('ListingTransaction', uselist=False, back_populates='coupon')

    __table_args__ = (
        UniqueConstraint('coupon_key'),
    )

    def __init__(
            self,
            percentage_off,
            coupon_key=None,
            unlimited=False,
            uses=0
    ):
        if coupon_key is None:
            self.coupon_key = self.genCouponKey()
        else:
            keyCount = session.query(Coupon).filter_by(coupon_key=coupon_key).count()

            if keyCount == 0:
                self.coupon_key = coupon_key
            else:
                newRandomKey = self.genCouponKey()
                self.coupon_key = newRandomKey
                flash('coupon Key is already in use, generated a different key : %s' % self.coupon_key, 'warning')

        self.percentage_off = percentage_off
        self.unlimited = unlimited
        self.uses = uses

        # Default Values
        now = dt.now().isoformat()  # Current Time to Insert into Datamodels
        self.date_created = now
        self.date_modified = now

    def __repr__(self):
        return '<Coupon id: %d | key: %s>' % (self.id, self.coupon_key)

    @property
    def serialize(self):
        return {
            'couponKey': self.coupon_key,
            'percentageOff': self.percentage_off,
            'uses': self.uses,
            'unlimited': self.unlimited
        }

    def genCouponKey(self):
        newRandomKey = idGenerator()

        keyCount = session.query(Coupon).filter_by(coupon_key=newRandomKey).count()

        while keyCount > 0:
            newRandomKey = idGenerator()

            keyCount = session.query(Coupon).filter_by(coupon_key=newRandomKey).count()

        return newRandomKey

    def couponPrice(self, price):
        return price * (1 - (self.percentage_off / 100))


def update_date_modified(mapper, connection, target):
    # 'target' is the inserted object
    target.date_modified = dt.now().isoformat()  # Update Date Modified


event.listen(Coupon, 'before_update', update_date_modified)
