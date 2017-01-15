from nexnest.application import session

from nexnest.data_gen.factories import UserFactory, ListingFactory, LandlordFactory, LandlordListingFactory, GroupFactory, GroupUserFactory, GroupListingFactory, MessageFactory, GroupMessageFactory, SchoolFactory, SchoolUserFactory


# USERS
landlord = UserFactory()
user2 = UserFactory()
user3 = UserFactory()
user4 = UserFactory()
user5 = UserFactory()
user6 = UserFactory()
user7 = UserFactory()
user8 = UserFactory()

# Schools
s = SchoolFactory()
session.commit()

# SCHOOL USERS
su1 = SchoolUserFactory(school=s, user=user2)
su2 = SchoolUserFactory(school=s, user=user3)
su3 = SchoolUserFactory(school=s, user=user4)
su4 = SchoolUserFactory(school=s, user=user5)
su5 = SchoolUserFactory(school=s, user=user6)
su6 = SchoolUserFactory(school=s, user=user7)
su7 = SchoolUserFactory(school=s, user=user8)

session.commit()

# LANDLORDS
landlord1 = LandlordFactory(user=landlord)

session.commit()

# LISTINGS
listing1 = ListingFactory()
listing2 = ListingFactory()
listing3 = ListingFactory()
listing4 = ListingFactory()

session.commit()

# LANDLORD LISTINGS
landlordListing1 = LandlordListingFactory(landlord=landlord1, listing=listing1)
landlordListing2 = LandlordListingFactory(landlord=landlord1, listing=listing2)
landlordListing3 = LandlordListingFactory(landlord=landlord1, listing=listing3)
landlordListing4 = LandlordListingFactory(landlord=landlord1, listing=listing4)

session.commit()

# GROUP
group1 = GroupFactory(leader=user2)
group2 = GroupFactory(leader=user3)
group3 = GroupFactory(leader=user4)

session.commit()

# GROUP USERS

# Group 1
groupuser1 = GroupUserFactory(group=group1, user=user2)
groupuser2 = GroupUserFactory(group=group1, user=user3)
groupuser3 = GroupUserFactory(group=group1, user=user4)
groupuser4 = GroupUserFactory(group=group1, user=user5)

# Group 2
groupuser5 = GroupUserFactory(group=group2, user=user3)
groupuser6 = GroupUserFactory(group=group2, user=user2)

# Group3
groupuser7 = GroupUserFactory(group=group3, user=user2)
groupuser8 = GroupUserFactory(group=group3, user=user8)
groupuser9 = GroupUserFactory(group=group3, user=user3)
groupuser10 = GroupUserFactory(group=group3, user=user4)
groupuser11 = GroupUserFactory(group=group3, user=user5)

groupuser1.accepted = True
groupuser2.accepted = True
groupuser3.accepted = True
groupuser4.accepted = True

groupuser6.accepted = True
groupuser7.accepted = True
groupuser8.accepted = True

groupuser10.accepted = True
groupuser11.accepted = True

session.commit()

# GROUP LISTING
groupListing = GroupListingFactory(group=group1, listing=listing1)

session.commit()

# GROUP MESSAGES
gmsg1 = GroupMessageFactory(group=group1, user=user2)
gmsg2 = GroupMessageFactory(group=group1, user=user3)
gmsg3 = GroupMessageFactory(group=group1, user=user2)
gmsg4 = GroupMessageFactory(group=group1, user=user4)
gmsg5 = GroupMessageFactory(group=group1, user=user2)
gmsg6 = GroupMessageFactory(group=group1, user=user5)

session.commit()

