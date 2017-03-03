from datetime import datetime as dt

from sqlalchemy import event
from sqlalchemy.orm import relationship

from flask import flash

from nexnest.application import db

from .base import Base


class House(Base):
    __tablename__ = 'houses'
    id = db.Column(db.Integer, primary_key=True)
    listing_id = db.Column(db.Integer, db.ForeignKey('listings.id'))
    group_id = db.Column(db.Integer, db.ForeignKey('groups.id'))
    date_created = db.Column(db.DateTime)
    date_modified = db.Column(db.DateTime)
    messages = relationship("HouseMessage", backref='house')
    maintenanceRequests = relationship("Maintenance", backref='house')

    def __init__(
            self,
            listing,
            group
    ):
        self.listing_id = listing.id
        self.group_id = group.id

        # Default Values
        now = dt.now().isoformat()  # Current Time to Insert into Datamodels
        self.date_created = now
        self.date_modified = now

    def __repr__(self):
        return '<House %r>' % self.id

    def isViewableBy(self, user):
        if user in self.group.acceptedUsers:
            return True
        elif user in self.listing.landLordsAsUsers():
            return True

        flash("Permissions Error", 'danger')
        return False

    @property
    def tenants(self):
        return self.group.acceptedUsers

    def activeMaintenanceRequests(self):
        maintenanceRequests = []
        for maintenanceRequest in self.maintenanceRequests:
            if maintenanceRequest.status is not 'completed':
                maintenanceRequests.append(maintenanceRequest)

        return maintenanceRequests

    def groupedMaintenanceRequests(self):
        openMR = []
        inProgressMR = []
        completedMR = []

        for mr in self.maintenanceRequests:
            # print('Maintenance Request %r ~ Status %s' % (mr, mr.status))
            if mr.status == 'open':
                openMR.append(mr)
            elif mr.status == 'inprogress':
                inProgressMR.append(mr)
            else:
                completedMR.append(mr)

        # print(openMR)
        # print(inProgressMR)
        # print(completedMR)
        return openMR, inProgressMR, completedMR


def update_date_modified(mapper, connection, target):  # pylint: disable=unused-argument
    # 'target' is the inserted object
    target.date_modified = dt.now().isoformat()  # Update Date Modified


event.listen(House, 'before_update', update_date_modified)
