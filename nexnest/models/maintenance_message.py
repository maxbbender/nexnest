from nexnest.application import db

from .message import Message


class MaintenanceMessage(Message):
    __tablename__ = 'maintenance_messages'
    message_id = db.Column(db.Integer,
                           db.ForeignKey('messages.id'),
                           primary_key=True)
    maintenance_id = db.Column(db.Integer,
                               db.ForeignKey('maintenances.id'),
                               primary_key=True)

    __mapper_args__ = {
        'polymorphic_identity': 'maintenance',
    }

    def __init__(
            self,
            maintenance,
            content,
            user
    ):
        super().__init__(
            content=content,
            user=user
        )

        self.maintenance_id = maintenance.id

    def __repr__(self):
        return '<MaintenanceMessage ~ Message %r | Maintenance %r>' % \
            (self.message_id, self.maintenance_id)
