from datetime import datetime as dt

from sqlalchemy import event
from sqlalchemy.orm import relationship

from flask import flash

from nexnest import db
from nexnest.models.notification import Notification
from nexnest.utils.misc import isWithin30Days

from .base import Base

session = db.session


class House(Base):
    __tablename__ = 'houses'
    id = db.Column(db.Integer, primary_key=True)
    listing_id = db.Column(db.Integer, db.ForeignKey('listings.id'))
    group_id = db.Column(db.Integer, db.ForeignKey('groups.id'))
    date_created = db.Column(db.DateTime)
    date_modified = db.Column(db.DateTime)
    messages = relationship("HouseMessage", backref='house')
    maintenanceRequests = relationship("Maintenance", backref='house')
    rent = relationship('Rent', backref='house')

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

    def genNotifications(self):
        for user in self.group.acceptedUsers:
            if user.notificationPreference.house_notification:
                newNotif = Notification(target_user=user,
                                        target_model_id=self.id,
                                        notif_type='house')
                session.add(newNotif)
                session.commit()

            if user.notificationPreference.house_email:
                user.sendEmail(emailType='house',
                               message=self.genEmailAcceptedContent(user))

        for user in self.listing.landLordsAsUsers():
            if user.notificationPreference.house_notification:
                newNotif = Notification(target_user=user,
                                        target_model_id=self.id,
                                        notif_type='house')
                session.add(newNotif)
                session.commit()

            if user.notificationPreference.house_email:
                user.sendEmail(emailType='house',
                               message=self.genLandlordEmailAcceptedContent(user))

    @property
    def groupedRentPayments(self):
        now = dt.now()
        upcomingPayments = []
        overduePayments = []
        completedPayments = []
        futurePayments = []

        for rent in self.rent:

            # Overdue Check
            if not rent.completed:

                if rent.date_due < now.date():
                    overduePayments.append(rent)
                    continue

                if isWithin30Days(rent.date_due):
                    upcomingPayments.append(rent)
                    continue

                futurePayments.append(rent)
            else:
                completedPayments.append(rent)

        return upcomingPayments, overduePayments, futurePayments, completedPayments

    def genEmailAcceptedContent(self, user):
        return """
        <div class="row">
            <div class="col-xs-1"></div>
            <div class="col-xs-10">
                <span>Hi  %s ,</span>
                <br><br>
                <span>
                    <strong>Congratulations!</strong> %s has approved your request to live at %s. Enjoy your new college nest!
                    <br><br>
                    Don't just tweet about it. Contact your landlord about putting down a deposit and signing your lease
                    <br><br>
                    Enjoy your %d school year!
                </span>
                <br><br>
            </div>
        </div>
        """ % (
            user.fname,
            self.listing.landLordsAsUsers()[0].name,
            self.listing.briefStreet,
            self.listing.start_date.year
        )

    def genLandlordEmailAcceptedContent(self, user):
        return """
        <div class="row">
            <div class="col-xs-1"></div>
            <div class="col-xs-10">
                <span>Hi  %s ,</span>
                <br><br>
                <strong>Congratulations!</strong> You have approved %s to live at %s for the %s lease term.
                            <br><br>
                            Feel free to contact this group to obtain a signed lease and security deposits from your new tenants.
                            <br><br>
                            <a href="https://nexnest.com/house/view/%d">Click here</a> to go the portal for the house and message this group!
                            <br><br>
                            Enjoy your %d school year!
                        </span>
                <br><br>
            </div>
        </div>
        """ % (
            user.fname,
            self.group.name,
            self.listing.briefStreet,
            self.group.humanTimePeriod,
            self.id,
            self.listing.start_date.year

        )


def update_date_modified(mapper, connection, target):  # pylint: disable=unused-argument
    # 'target' is the inserted object
    target.date_modified = dt.now().isoformat()  # Update Date Modified


event.listen(House, 'before_update', update_date_modified)
