from datetime import datetime as dt

from nexnest.application import db

from .base import Base

from sqlalchemy import event


class Transaction(Base):
    __tablename__ = 'transactions'
    id = db.Column(db.Integer, primary_key=True)
    braintree_transaction_id = db.Column(db.Text)
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
            braintree_transaction_id,
            status,
            type,
            user,
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
            braintree_transaction_id,
            status,
            success

    ):

        super().__init__(
            braintree_transaction_id=braintree_transaction_id,
            status=status,
            success=success
        )

        self.listing_id = listing.id
        self.plan = plan
