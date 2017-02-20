from sqlalchemy import *
from migrate import *


def upgrade(migrate_engine):
    meta = MetaData(bind=migrate_engine)

    # users = Table('users', meta, autoload=True)
    listings = Table('listings', meta, autoload=True)

    # password = Column("password", String(128), nullable=False)
    ptype = Column("property_type", Text())
    rent = Column("rent_due", String(20))
    maintenance = Column('maintenance', Boolean())
    first_semester_rent_due_date = Column('first_semester_rent_due_date', Date())
    second_semester_rent_due_date = Column('second_semester_rent_due_date', Date())
    monthly_rent_due_date = Column('monthly_rent_due_date', Date())

    ptype.create(listings)
    rent.create(listings)
    maintenance.create(listings)
    monthly_rent_due_date.create(listings)
    second_semester_rent_due_date.create(listings)
    first_semester_rent_due_date.create(listings)

    pass


def downgrade(migrate_engine):
    meta = MetaData(bind=migrate_engine)

    # users = Table('users', meta, autoload=True)
    listings = Table('listings', meta, autoload=True)

    # users.c.password.drop()
    listings.c.ptype.drop()
    listings.c.rent.drop()
    listings.c.maintenance.drop()
    listings.c.monthly_rent_due_date.drop()
    listings.c.second_semester_rent_due_date.drop()
    listings.c.first_semester_rent_due_date.drop()

    pass
