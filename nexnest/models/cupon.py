from datetime import datetime as dt

from nexnest.application import db

from .base import Base

from sqlalchemy import event, UniqueConstraint


class Cupon(Base):
    __tablename__ = 'cupons'
    id = db.Column(db.Integer, primary_key=True)
    cupon_key = db.Column(db.Text)
    unlimited = db.Column(db.Boolean)
    uses = db.Column(db.Integer)
    date_created = db.Column(db.DateTime)
    date_modified = db.Column(db.DateTime)

    __table_args__ = (
        UniqueConstraint('cupon_key'),
    )

    def __init__(
            self,
            cupon_key=None,
            unlimited=False,
            uses=0
    ):
        self.cupon_key = cupon_key
        self.unlimited = unlimited
        self.uses = uses

        # Default Values
        now = dt.now().isoformat()  # Current Time to Insert into Datamodels
        self.date_created = now
        self.date_modified = now

    def __repr__(self):
        return '<Cupon id:%d | key:%s>' % (self.id, self.cupon_key)


def update_date_modified(mapper, connection, target):
    # 'target' is the inserted object
    target.date_modified = dt.now().isoformat()  # Update Date Modified


event.listen(Cupon, 'before_update', update_date_modified)


# Table('cupons', MetaData(bind=None), Column('id', Integer(), table=<cupons>, primary_key=True, nullable=False), Column('cupon_key', Text(), table=<cupons>), Column('unlimited', Boolean(), table=<cupons>), Column('uses', Integer(), table=<cupons>), Column('date_created', DateTime(), table=<cupons>), Column('date_modified', DateTime(), table=<cupons>), schema=None)
