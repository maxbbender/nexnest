from nexnest.application import db

from .base import Base


class MaintenanceMessage(Base):
    __tablename__ = 'maintenance_messages'
    message_id = db.Column(db.Integer,
                           db.ForeignKey('messages.id'),
                           primary_key=True)
    maintenance_id = db.Column(db.Integer,
                               db.ForeignKey('maintenances.id'),
                               primary_key=True)

    def __init__(
            self,
            message,
            maintenance
    ):

        self.message_id = message.id
        self.maintenance_id = maintenance.id

    def __repr__(self):
        return '<MaintenanceMessage ~ Message %r | Maintenance %r>' % \
            (self.message_id, self.maintenance_id)
