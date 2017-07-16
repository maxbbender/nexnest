from nexnest.models.house import House
from nexnest.models.rent import Rent

from nexnest.application import session


def createHouse(listing, group):
    # Create the house object
    house = House(listing=listing,
                  group=group)

    session.add(house)
    session.commit()

    # Now let's create the rent payments based off the house pay period
    if listing.rent_due == 'monthly':
        currentDate = listing.start_date

        for user in house.tenants:
            while currentDate < listing.end_date:
                dateDue = currentDate.replace(day=1)

                newRent = Rent(house, user, dateDue)
                # session.add(newRent)
                session.commit()
                pass

    else:
        for user in house.tenants:
            firstSemesterRent = Rent(house, user, listing.first_semester_rent_due_date)
            session.add(firstSemesterRent)

            secondSemesterRent = Rent(house, user, listing.second_semester_rent_due_date)
            session.add(secondSemesterRent)

            session.commit()

    return house
