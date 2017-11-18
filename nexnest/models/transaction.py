from datetime import datetime as dt

from nexnest import db

from .base import Base

from sqlalchemy import event
from sqlalchemy.orm import relationship

from flask import flash
from flask import current_app as app

from nexnest.static.dataSets import schoolUpgradePrice, summerUpgradePrice


class Transaction(Base):
    __tablename__ = 'transactions'
    id = db.Column(db.Integer, primary_key=True)
    braintree_transaction_id = db.Column(db.Text)
    # open | authorized | submitted| settling | settled
    status = db.Column(db.String(128))
    success = db.Column(db.Boolean)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    type = db.Column(db.String(60))
    total = db.Column(db.Float)
    date_created = db.Column(db.DateTime)
    date_modified = db.Column(db.DateTime)

    __mapper_args__ = {
        'polymorphic_identity': 'transactions',
        'polymorphic_on': type
    }

    def __init__(
            self,
            status,
            user,
            total=None,
            braintree_transaction_id=None,
            success=False,
    ):
        self.user_id = user.id
        self.braintree_transaction_id = braintree_transaction_id
        self.status = status
        self.success = success
        self.total = total

        # Default Values
        now = dt.now().isoformat()  # Current Time to Insert into Datamodels
        self.date_created = now
        self.date_modified = now

    def __repr__(self):
        return '<Transaction %r>' % self.id

    def isViewableBy(self, user):
        if self.user == user:
            return True
        else:
            flash("Invalid Permissions")
            return False


def update_date_modified(mapper, connection, target):
    # 'target' is the inserted object
    target.date_modified = dt.now().isoformat()  # Update Date Modified


event.listen(Transaction, 'before_update', update_date_modified)


class ListingTransaction(Transaction):
    __tablename__ = 'listing_transactions'
    id = db.Column(db.Integer, db.ForeignKey('transactions.id'), primary_key=True)
    coupon_id = db.Column(db.Integer, db.ForeignKey('coupons.id'))
    listings = relationship("ListingTransactionListing", backref='transaction')
    coupon = relationship('Coupon', back_populates='listingTransaction')

    __mapper_args__ = {
        'polymorphic_identity': 'listing',
    }

    def __init__(
            self,
            user,
            status='open',
            success=False,
            braintree_transaction_id=None,
            coupon=None
    ):

        super().__init__(
            braintree_transaction_id=braintree_transaction_id,
            status=status,
            success=success,
            user=user
        )

        if coupon is not None:
            self.coupon_id = coupon.id

    def __repr__(self):
        return 'ListingTransaction %r' % self.id

    @property
    def totalTransactionPrice(self):
        app.logger.debug("totalTransactionPrice()")
        if self.total is not None:
            app.logger.debug("self.total is %d" % self.total)
            return self.total
        else:
            totalPrice = 0
            # STANDARD 120 | 90 | 30
            # PRIVELEGED 200 | 160 | 70
            for listing in self.listings:
                app.logger.debug("looking at listing %r" % listing.listing)                
                if listing.listing.time_period == 'school':
                    totalPrice += schoolUpgradePrice
                elif listing.listing.time_period == 'summer':
                    totalPrice += summerUpgradePrice
                
                app.logger.debug("New Total : %r" % totalPrice)

            if self.coupon is not None:
                self.total = self.coupon.couponPrice(totalPrice)
                app.logger.debug("Price after Coupon %r" % self.total)
            else:
                self.total = totalPrice

            app.logger.debug('Applying tax to the price')
            self.total = self.total * 1.075
            app.logger.debug('Price after tax : %r' % self.total)

            self.total = float("%.2f" % self.total)

            db.session.commit()

            return self.total


class ListingTransactionListing(Base):
    __tablename__ = 'listing_transaction_listings'
    id = db.Column(db.Integer, primary_key=True)
    listing_id = db.Column(db.Integer, db.ForeignKey('listings.id'))
    plan = db.Column(db.String(50))
    listing_transactions_id = db.Column(db.Integer, db.ForeignKey('listing_transactions.id'))

    def __init__(self,
                 listing,
                 listingTransaction,
                 plan):

        self.listing_id = listing.id
        self.listing_transactions_id = listingTransaction.id
        self.plan = plan

    def __repr__(self):
        return 'ListingTransactionListings %d ~ ListingID %d | ListingTransactionID %d' % \
            (self.id, self.listing_id, self.listing_transactions_id)


class RentTransaction(Transaction):
    __tablename__ = 'rent_transactions'
    id = db.Column(db.Integer, db.ForeignKey('transactions.id'), primary_key=True)
    rent_id = db.Column(db.Integer, db.ForeignKey('rents.id'))
    rent = relationship("Rent", back_populates="transaction")

    __mapper_args__ = {
        'polymorphic_identity': 'rent',
    }

    def __init__(
            self,
            user,
            status='open',
            success=False,
            braintree_transaction_id=None,
            coupon=None
    ):

        super().__init__(
            braintree_transaction_id=braintree_transaction_id,
            status=status,
            success=success,
            user=user
        )

    def __repr__(self):
        return 'Rent Transaction %d ~ Rent %r' % (self.id, self.rent)
