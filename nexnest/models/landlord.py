from datetime import datetime as dt
from sqlalchemy.orm import relationship

from nexnest.application import db

from .base import Base


class Landlord(Base):
    __tablename__ = 'landlords'
    user_id = db.Column(db.Integer,
                        db.ForeignKey('users.id'),
                        primary_key=True)
    online_pay = db.Column(db.Boolean)
    check_pay = db.Column(db.Boolean)
    street = db.Column(db.Text)
    city = db.Column(db.Text)
    state = db.Column(db.String(2))
    zip_code = db.Column(db.String(5))
    listings = relationship("LandlordListing", back_populates='landlord')

    def __init__(self,
                 user,
                 online_pay,
                 check_pay,
                 street,
                 city,
                 state,
                 zip_code):

        self.user = user
        self.user_id = user.id
        self.online_pay = online_pay
        self.check_pay = check_pay
        self.street = street
        self.city = city
        self.state = state
        self.zip_code = zip_code

    def __repr__(self):
        return '<Landlord %r>' % self.user_id

    def getListings(self):
        listings = []
        for landlordListing in self.listings:
            listings.append(landlordListing.listing)

        return listings

    def getActiveTours(self):
        requestedTours = []
        scheduledTours = []

        for listing in self.getListings():
            if not listing.hasHouse():
                requestedToursObject = {'listing': listing}
                scheduledToursObject = {'listing': listing}

                rqTours = []
                schTours = []

                for tour in listing.tours:
                    if tour.time_requested >= dt.now():
                        if tour.tour_confirmed:
                            schTours.append(tour)
                        else:
                            rqTours.append(tour)

                if len(rqTours) > 0:
                    requestedToursObject['tours'] = rqTours
                    requestedTours.append(requestedToursObject)

                if len(schTours) > 0:
                    scheduledToursObject['tours'] = schTours
                    scheduledTours.append(scheduledToursObject)
            else:
                continue

        if len(requestedTours) > 0 and len(scheduledTours) > 0:
            return requestedTours, scheduledTours
        elif len(requestedTours) > 0 and len(scheduledTours) == 0:
            return requestedTours, None
        elif len(requestedTours) == 0 and len(scheduledTours) > 0:
            return None, scheduledTours
        else:
            return None, None

    def getHousingRequests(self):
        unAcceptedHousingRequests = []
        acceptedHousingRequests = []
        completedHousingRequests = []

        for listing in self.getListings():
            if not listing.hasHouse():
                listingDict = {'listing': listing}
                houseRequests = []

                for houseRequest in listing.groups:
                    if houseRequest.landlord_show and houseRequest.group_show:
                        if houseRequest.accepted:
                            acceptedHousingRequests.append(houseRequest)
                            houseRequest = []
                            break
                        else:
                            houseRequests.append(houseRequest)

                if len(houseRequests) > 0:
                    listingDict['houseRequests'] = houseRequests
                    unAcceptedHousingRequests.append(listingDict)

            else:
                for houseRequest in listing.groups:
                    if houseRequest.completed:
                        completedHousingRequests.append(houseRequest)
                        break

        return unAcceptedHousingRequests, acceptedHousingRequests, completedHousingRequests

    def getHouses(self):
        houses = []
        for listing in self.getListings():
            if listing.hasHouse():
                houses.append(listing.house[0])
                # if len(listing.house) > 0:
                #     for house in listing.house:
                #         houses.append(listing.house)
                # else:
                #     houses.append(listing.house[0])
        if len(houses) > 0:
            return houses
        else:
            return None

    def getMaintenanceRequests(self):
        openMaintenanceRequests = []
        inProgressMaintenanceRequests = []
        completedMaintenanceRequests = []

        for house in self.getHouses():
            openMR, inProgressMR, completedMR = house.groupedMaintenanceRequests()
            
            if len(openMR) > 0:
                houseObject = {'house': house}
                houseObject['maintenanceRequests'] = openMR
                openMaintenanceRequests.append(houseObject)

            if len(inProgressMR) > 0:
                houseObject = {'house': house}
                houseObject['maintenanceRequests'] = inProgressMR
                inProgressMaintenanceRequests.append(houseObject)

            if len(completedMR) > 0:
                houseObject = {'house': house}
                houseObject['maintenanceRequests'] = completedMR
                completedMaintenanceRequests.append(houseObject)

        return openMaintenanceRequests, inProgressMaintenanceRequests, completedMaintenanceRequests
