from .base import Base
from datetime import datetime as dt
from nexnest.application import db

from sqlalchemy.orm import relationship


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
        activeTours = []

        for listing in self.getListings():
            if not listing.hasHouse():
                listingDict = {'listing': listing}
                tours = []
                for tour in listing.tours:
                    if tour.time_requested >= dt.now():
                        tours.append(tour)

                if len(tours) == 0:
                    continue

                listingDict['tours'] = tours
            else:
                continue

            activeTours.append(listingDict)

        if len(activeTours) > 0:
            return activeTours
        else:
            return None

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
                            print('appending')
                            houseRequests.append(houseRequest)

                if len(houseRequests) > 0:
                    listingDict['houseRequests'] = houseRequests
                    unAcceptedHousingRequests.append(listingDict)

            else:
                for houseRequest in listing.groups:
                    print(houseRequest.completed)
                    if houseRequest.completed:
                        completedHousingRequests.append(houseRequest)
                        break

        return unAcceptedHousingRequests, acceptedHousingRequests, completedHousingRequests
