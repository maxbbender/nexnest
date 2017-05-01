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
                 Column('price_per_month', Integer()),
                 Column('price_per_semester', Integer()),
                 Column('square_footage', Integer()),
                 Column('parking', String()),
                 Column('time_period_date_range', Text()),
                 Column('cats', Boolean()),
                 Column('dogs', Boolean()),
                 Column('other_pets', Text()),
                 Column('washer', Boolean()),
                 Column('dryer', Boolean()),
                 Column('dishwasher', Boolean()),
                 Column('air_conditioning', Boolean()),
                 Column('handicap', Boolean()),
                 Column('furnished', Boolean()),
                 Column('emergency_maintenance', Boolean()),
                 Column('snow_plowing', Boolean()),
                 Column('garbage_service', Boolean()),
                 Column('security_service', Boolean()),
                 Column('date_created', DateTime()),
                 Column('date_modified', DateTime()),
                 Column('electricity', Boolean()),
                 Column('internet', Boolean()),
                 Column('water', Boolean()),
                 Column('heat_gas', Boolean()),
                 Column('cable', Boolean()),
                 Column('washer_free', Boolean()),
                 Column('featured', Boolean()),
                 Column('youtube_url', String(length=256)),
                 Column('floor_plan_url', String(length=256)),
                 Column('lat', Numeric()),
                 Column('lng', Numeric()),
                 Column('banner_photo_url', Text()))


def upgrade(migrate_engine):
    meta.bind = migrate_engine

    listings.create()

    # Foreign Keys
    # schools = Table('schools', meta, autoload=True)

    # ForeignKeyConstraint(
    #     columns=[listings.c.school_id],
    #     refcolumns=[schools.c.id]).create()


def downgrade(migrate_engine):
    meta.bind = migrate_engine

    # Foreign Keys
    # schools = Table('schools', meta, autoload=True)

    # ForeignKeyConstraint(
    #     columns=[listings.c.school_id],
    #     refcolumns=[schools.c.id]).drop()

    listings.drop()
