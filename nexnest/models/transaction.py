from datetime import datetime as dt

from nexnest.application import db

from .base import Base

from sqlalchemy import event


class Transaction(Base):
    __tablename__ = 'transactions'
    id = db.Column(db.Integer, primary_key=True)
    braintree_transaction_id = db.Column(db.Text)
    # open | authorized | submitted| settling | settled
    status = db.Column(db.String(128))
    success = db.Column(db.Boolean)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    type = db.Column(db.String(60))
    date_created = db.Column(db.DateTime)
    date_modified = db.Column(db.DateTime)

    __mapper_args__ = {
        'polymorphic_identity': 'transactions',
        'polymorphic_on': type
    }

    def __init__(
            self,
            status,
            type,
            user,
            braintree_transaction_id=None,
            success=False,
    ):
        self.user_id = user.id
        self.braintree_transaction_id = braintree_transaction_id
        self.status = status
        self.success = success

        # Default Values
        now = dt.now().isoformat()  # Current Time to Insert into Datamodels
        self.date_created = now
        self.date_modified = now

    def __repr__(self):
        return '<Transaction %r>' % self.id


def update_date_modified(mapper, connection, target):
    # 'target' is the inserted object
    target.date_modified = dt.now().isoformat()  # Update Date Modified


event.listen(Transaction, 'before_update', update_date_modified)


class ListingTransaction(Transaction):
    __tablename__ = 'listing_transactions'
    id = db.Column(db.Integer, db.ForeignKey('transactions.id'), primary_key=True)
    listing_id = db.Column(db.Integer, db.ForeignKey('listings.id'))
    plan = db.Column(db.String(50))

    __mapper_args__ = {
        'polymorphic_identity': 'listing',
    }

    def __init__(
            self,
            listing,
            plan,
            user,
            status='open',
            success=False,
            braintree_transaction_id=None
    ):

        super().__init__(
            braintree_transaction_id=braintree_transaction_id,
            status=status,
            success=success,
            user=user
        )

        self.listing_id = listing.id
        self.plan = plan

    def __repr__(self):
        return 'ListingTransaction %r | %s' % (self.id, self.plan)


class ListingTransactionListings(Base):
    __tablename__ = 'listing_transaction_listings'
    id = db.Column(db.Integer, primary_key=True)
    listing_id = db.Column(db.Integer, db.ForeignKey('listings.id'))
    listing_transactions_id = db.Column(db.Integer, db.ForeignKey('listing_transactions.id'))

    def __init__(self,
                 listing,
                 listingTransaction):

        self.listing_id = listing.id
        self.listing_transactions_id = listingTransaction.id

    def __repr__(self):
        return 'ListingTransactionListings %d ~ ListingID %d | ListingTransactionID %d' % \
            (self.id, self.listing_id, self.listing_transactions_id)
