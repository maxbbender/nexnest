from datetime import datetime as dt

from sqlalchemy import event
from sqlalchemy.orm import relationship

from flask import flash

from nexnest.application import db, session
from nexnest.models.notification import Notification

from .base import Base


class Tour(Base):
    __tablename__ = 'tours'
    id = db.Column(db.Integer, primary_key=True)
    listing_id = db.Column(db.Integer, db.ForeignKey('listings.id'))
    group_id = db.Column(db.Integer, db.ForeignKey('groups.id'))
    date_created = db.Column(db.DateTime)
    date_modified = db.Column(db.DateTime)
    tour_confirmed = db.Column(db.Boolean)
    last_requested = db.Column(db.String(8))
    declined = db.Column(db.Boolean)
    messages = relationship('TourMessage', backref='tour')
    tourTimes = relationship('TourTime', backref='tour')

    def __init__(
            self,
            listing,
            group
    ):
        self.listing = listing
        self.group = group

        self.last_requested = 'group'
        self.tour_confirmed = False
        self.declined = False

        # Default Values
        now = dt.now().isoformat()  # Current Time to Insert into Datamodels
        self.date_created = now
        self.date_modified = now

    def __repr__(self):
        return '<Tour %r>' % self.id

    def serialize(self):
        group_users = []
        for user in self.group.acceptedUsers:
            group_users.append(user.shortSerialize)

        requestedTimes = []
        for time in self.tourTimes:
            requestedTimes.append(time.serialize)

        tour = {
            'id': self.id,
            'lastRequested': self.last_requested,
            'tourConfirmed': self.tour_confirmed,
            'url': '/tour/view/%d' % self.id,
            'group': self.group.serialize,
            'requestedTimes': requestedTimes
        }

        if self.hasConfirmedTourTime:
            tour['confirmedTime'] = self.confirmedTourTime.serialize

        return tour

    @property
    def confirmedTourTime(self):
        for tourTime in self.tourTimes:
            if tourTime.confirmed:
                return tourTime

        return None

    @property
    def hasConfirmedTourTime(self):
        for tourTime in self.tourTimes:
            if tourTime.confirmed:
                return True

        return False

    @property
    def groupedTourTimes(self):
        tourDicts = []

        for tourTime in self.tourTimes:
            foundDate = next((item for item in tourDicts if item["date"] == tourTime.humanDateOnlyString), None)

            if foundDate is not None:
                foundDate['times'].append(tourTime.humanTimeOnlyString)
            else:
                tourDicts.append({'date': tourTime.humanDateOnlyString, 'times': [tourTime.humanTimeOnlyString]})

        return tourDicts

    def isViewableBy(self, user, toFlash=True):
        if user in self.group.getUsers() or user in self.listing.landLordsAsUsers():
            return True
        elif toFlash:
            flash("Permissions Error")

        return False

    def isEditableBy(self, user, toFlash=True):
        if user == self.group.leader or user in self.listing.landLordsAsUsers():
            return True
        elif toFlash:
            flash("Permissions Error", 'danger')

        return False

    def genNotifications(self):
        for landlord in self.listing.landLordsAsUsers():

            if landlord.notificationPreference.tour_create_notification:
                newNotif = Notification(notif_type='tour',
                                        target_user=landlord,
                                        target_model_id=self.id)
                session.add(newNotif)
                session.commit()

            if landlord.notificationPreference.tour_create_email:
                landlord.sendEmail(emailType='tourRequest',
                                   message=self.genTourEmailCreatedContent(user=landlord))

    def genConfirmNotifications(self):
        for user in self.group.acceptedUsers:

            if user.notificationPreference.tour_confirmed_notification:
                newNotif = Notification(notif_type='tour_confirmed',
                                        target_user=user,
                                        target_model_id=self.id)
                session.add(newNotif)
                session.commit()

            if user.notificationPreference.tour_confirmed_email:
                user.sendEmail(emailType='tourConfirmed',
                               message=self.genTourEmailConfirmedContent())

    def undoConfirmNotifications(self):
        session.query(Notification) \
            .filter_by(notif_type='tour_confirmed',
                       target_model_id=self.id) \
            .delete()
        session.commit()

    def genTimeChangeNotifications(self):
        if self.last_requested == 'landlord':
            for user in self.group.acceptedUsers:

                if user.notificationPreference.tour_time_notification:

                    newNotif = Notification(notif_type='new_tour_time',
                                            target_user=user,
                                            target_model_id=self.id)
                    session.add(newNotif)
                    session.commit()

                if user.notificationPreference.tour_time_email:
                    user.sendEmail(emailType='tourTimeChange',
                                   message=self.genTourEmailTimeChangeContent(user))

        else:
            for user in self.listing.landLordsAsUsers():

                if user.notificationPreference.tour_time_notification:
                    newNotif = Notification(notif_type='new_tour_time',
                                            target_user=user,
                                            target_model_id=self.id)
                    session.add(newNotif)
                    session.commit()

                if user.notificationPreference.tour_time_email:
                    user.sendEmail(emailType='tourTimeChange',
                                   message=self.genTourEmailTimeChangeContent(user))

    def undoTimeChangeNotifications(self):
        session.query(Notification) \
            .filter_by(notif_type='new_tour_time',
                       target_model_id=self.id) \
            .delete()
        session.commit()

    def genDeniedNotifications(self):
        for user in self.group.acceptedUsers:
            if user.notificationPreference.tour_denied_notification:
                newNotif = Notification(notif_type='tour_denied',
                                        target_user=user,
                                        target_model_id=self.id)
                session.add(newNotif)
                session.commit()

            if user.notificationPreference.tour_denied_email:
                user.sendEmail(emailType='tourDenied',
                               message=self.genTourEmailDeniedContent(user=user))

    def undoDeniedNotifications(self):
        session.query(Notification) \
            .filter_by(notif_type='tour_denied',
                       target_model_id=self.id) \
            .delete()
        session.commit()

    # EMAIL FUNCTION
    def genTourEmailCreatedContent(self, user):
        emailString = """
            <h4>Hi %s</h4>
            <br>
            You have recieved a tour request for %s<br>
            The following times have been requested by %s<br>

            """ % (user.name, self.listing.briefStreet, self.group.leader.name)

        for tourTimeDict in self.groupedTourTimes:
            emailString += """
                <div style="padding-left:40px">
                    <strong>%s</strong><br>
            """ % tourTimeDict['date']

            for time in tourTimeDict['times']:
                emailString += "%s<br>" % time

            emailString += "</div><br>"

        emailString += """
        If you'd like to message Jerry before approving the tour, click <a href="https://nexnest.com/user/directMessages/%d">here</a><br>

            Click <a href="https://nexnest.com/landlord/dashboard">here</a> to visit all tour requests.<br><br>
        """ % user.id

        return emailString

    def genTourEmailConfirmedContent(self):
        return  """
        <strong>Congratulations!</strong> The following tour time was approved by %s for %s on:
        <br><br>
        <div style="padding-left:20px">
        <strong>%s</strong><br>
        <strong>%s</strong>
        </div>
        <br><br>
        A reminder will be sent to you on the morning of your scheduled tour!<br><br>
        Feel free to contact the landlord by clicking <a href="https://nexnest.com/user/directMessages/%d">here</a> with any additional questions<br><br>
        Thanks for choosing <a href="https://nexnest.com">nexnest.com</a>.
        """ % (self.listing.landLordsAsUsers()[0].name,
               self.listing.briefStreet,
               self.confirmedTourTime.humanDateOnlyString,
               self.confirmedTourTime.humanTimeOnlyString,
               self.listing.landLordsAsUsers()[0].id)

    def genTourEmailDeniedContent(self, user):
        return """
        Hello %s,<br>
        We are sorery to inform you that your tour request was denied for %s. This listing may have been booked or is no longer available for rent from the owner.<br><br>
        Don't let that stop your housing search! Visit <a href="https://nexnest.com">nexnest.com</a> to find the newest available rentals in your area.<br><br>
        """ % (user.name, self.listing.briefStreet)

    def genTourEmailTimeChangeContent(self, user):
        return """
        Hi %s,<br><br>
        A new tour time has been requested for %s<br><br>
        Click <a href="https://nexnest.com/tour/view/%d">here</a> or the link below to confirm, decline or suggest a new time.<br><br>
        <a href="https://nexnest.com/tour/view/%d">https://nexnest.com/tour/view/%d></a><br><br>
        We hope you tour the property soon! Thanks for using <a href="https://nexnest.com">nexnest.com</a><br><br>
        """ % (
            user.name,
            self.listing.briefStreet,
            self.id,
            self.id,
            self.id
        )


def update_date_modified(mapper, connection, target):  # pylint: disable=unused-argument
    # 'target' is the inserted object
    target.date_modified = dt.now().isoformat()  # Update Date Modified


event.listen(Tour, 'before_update', update_date_modified)
