from nexnest.application import session

from nexnest.data_gen.factories import UserFactory, ListingFactory, LandlordFactory, LandlordListingFactory, GroupFactory, GroupUserFactory, GroupListingFactory, MessageFactory, GroupMessageFactory, SchoolFactory, DirectMessageFactory

# Schools
s = SchoolFactory()
session.commit()

# USERS
landlord = UserFactory(school=s)
user2 = UserFactory(school=s)
user3 = UserFactory(school=s)
user4 = UserFactory(school=s)
user5 = UserFactory(school=s)
user6 = UserFactory(school=s)
user7 = UserFactory(school=s)
user8 = UserFactory(school=s)

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

# DIRECT MESSAGES
dm1 = DirectMessageFactory(source_user=user2, target_user=user3)
dm2 = DirectMessageFactory(source_user=user3, target_user=user2)
dm3 = DirectMessageFactory(source_user=user2, target_user=user3)
dm4 = DirectMessageFactory(source_user=user3, target_user=user4)
dm5 = DirectMessageFactory(source_user=user4, target_user=user3)
dm6 = DirectMessageFactory(source_user=user2, target_user=user3)
dm6 = DirectMessageFactory(source_user=user2, target_user=user4)

session.commit()
