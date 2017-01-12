from nexnest.application import session

from nexnest.data_gen.factories import UserFactory, ListingFactory, LandlordFactory, LandlordListingFactory, GroupFactory, GroupUserFactory, GroupListingFactory

# USERS
user1 = UserFactory()
user2 = UserFactory()
user3 = UserFactory()
user4 = UserFactory()
user5 = UserFactory()
user6 = UserFactory()
user7 = UserFactory()

session.add(user1)
session.add(user2)
session.add(user3)
session.add(user4)
session.add(user5)
session.add(user6)
session.add(user7)
session.commit()

# LANDLORDS
landlord1 = LandlordFactory(user=user1)

session.add(landlord1)
session.commit()

# LISTINGS
listing1 = ListingFactory()
listing2 = ListingFactory()
listing3 = ListingFactory()
listing4 = ListingFactory()

session.add(listing1)
session.add(listing2)
session.add(listing3)
session.add(listing4)
session.commit()

# LANDLORD LISTINGS
landlordListing1 = LandlordListingFactory(landlord=landlord1, listing=listing1)
landlordListing2 = LandlordListingFactory(landlord=landlord1, listing=listing2)
landlordListing3 = LandlordListingFactory(landlord=landlord1, listing=listing3)
landlordListing4 = LandlordListingFactory(landlord=landlord1, listing=listing4)

session.add(landlordListing1)
session.add(landlordListing2)
session.add(landlordListing3)
session.add(landlordListing4)
session.commit()

# GROUP
group1 = GroupFactory(leader=user2)
group2 = GroupFactory(leader=user3)

session.add(group1)
session.add(group2)
session.commit()

# GROUP USERS
groupuser1 = GroupUserFactory(group=group1, user=user2)
groupuser2 = GroupUserFactory(group=group1, user=user3)
groupuser3 = GroupUserFactory(group=group1, user=user4)
groupuser4 = GroupUserFactory(group=group1, user=user5)

groupuser5 = GroupUserFactory(group=group2, user=user3)
groupuser6 = GroupUserFactory(group=group2, user=user2)

groupuser1.accepted = True
groupuser2.accepted = True
groupuser3.accepted = True
groupuser4.accepted = True
groupuser5.accepted = True

session.add(groupuser1)
session.add(groupuser2)
session.add(groupuser3)
session.add(groupuser4)
session.add(groupuser5)
session.commit()

# GROUP LISTING
groupListing = GroupListingFactory(group=group1, listing=listing1)
session.add(groupListing)
session.commit()
