from sqlalchemy import *
from migrate import *


meta = MetaData()
# Column('XXXX', String(120)),
listings = Table('listings', meta,
                 Column('id', Integer(),
                        primary_key=True,
                        nullable=False),
                 Column('street', Text()),
                 Column('city', Text()),
                 Column('state', String(length=2)),
                 Column('zip_code', String(length=5)),
                 Column('start_date', Date()),
                 Column('end_date', Date()),
                 Column('unit_type', String(length=10)),
                 Column('num_bedrooms', Integer()),
                 Column('price', Integer()),
                 Column('square_footage', Integer()),
                 Column('parking', String()),
                 Column('cats', Boolean()),
                 Column('dogs', Boolean()),
                 Column('other_pets', Boolean()),
                 Column('washer', Boolean()),
                 Column('dryer', Boolean()),
                 Column('dishwasher', Boolean()),
                 Column('air_conditioning', Boolean()),
                 Column('handicap', Boolean()),
                 Column('furnished', Boolean()),
                 Column('utilities_included', Boolean()),
                 Column('emergency_maintenance', Boolean()),
                 Column('snow_plowing', Boolean()),
                 Column('garbage_service', Boolean()),
                 Column('security_service', Boolean()),
                 Column('date_created', DateTime()),
                 Column('date_modified', DateTime()))


def upgrade(migrate_engine):
    meta.bind = migrate_engine
    listings.create()


def downgrade(migrate_engine):
    meta.bind = migrate_engine
    listings.drop()
