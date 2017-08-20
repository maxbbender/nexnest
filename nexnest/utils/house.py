from nexnest.models.house import House
from nexnest.models.rent import Rent

from nexnest import db
from nexnest.utils.misc import add_months

from flask import current_app as app

session = db.session


def createHouse(listing, group):
    # Make sure the house doesn't already exist
    houseCheck = House.query.filter_by(listing=listing, group=group).first()

    if houseCheck is None:
        # Create the house object
        house = House(listing=listing,
                      group=group)

        session.add(house)
        session.commit()

        house.genNotifications()

        house.listing.cancelTours()
        house.listing.cancelGroupListingRequests()

        house.group.cancelTours()
        house.group.cancelListingRequests()

        # Now let's create the rent payments based off the house pay period
        if listing.rent_due == 'monthly':
            app.logger.debug('Creating monthly rents')

            for user in house.tenants:
                currentDate = listing.start_date
                app.logger.debug('Creating rent records for user %r' % user)
                while currentDate < listing.end_date:
                    dateDue = currentDate.replace(day=1)

                    app.logger.debug('Rent for %r' % dateDue)

                    newRent = Rent(house, user, dateDue, listing.price_per_month)
                    session.add(newRent)
                    session.commit()

                    currentDate = add_months(currentDate, 1)
                    pass

        else:
            app.logger.debug('Creating semester rents')
            for user in house.tenants:
                firstSemesterRent = Rent(house, user, listing.first_semester_rent_due_date, listing.price_per_semester)
                session.add(firstSemesterRent)

                secondSemesterRent = Rent(house, user, listing.second_semester_rent_due_date, listing.price_per_semester)
                session.add(secondSemesterRent)

                session.commit()

        return house
    else:
        return None
