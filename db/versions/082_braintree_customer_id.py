from sqlalchemy import *
from migrate import *


def upgrade(migrate_engine):
    meta = MetaData(bind=migrate_engine)

    # users = Table('users', meta, autoload=True)
    users = Table('users', meta, autoload=True)

    # password = Column("password", String(128), nullable=False)
    braintree_customer_id = Column("braintree_customer_id", String(36), nullable=True)
    credit_verification_id = Column("credit_verification_id", Text(), nullable=True)

    # password.create(users)
    braintree_customer_id.create(users)
    credit_verification_id.create(users)
    pass


def downgrade(migrate_engine):
    meta = MetaData(bind=migrate_engine)

    # users = Table('users', meta, autoload=True)
    users = Table('users', meta, autoload=True)

    # users.c.password.drop()
    users.c.braintree_customer_id.drop()
    users.c.credit_verification_id.drop()
    pass
