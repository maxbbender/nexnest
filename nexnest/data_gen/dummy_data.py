from nexnest.application import session

from nexnest.data_gen.factories import *

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
admin = UserFactory(role='admin', email='admin@admin.com')

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

# TOURS
t1 = TourFactory(listing=listing1, group=group1)
t2 = TourFactory(listing=listing1, group=group2)
t3 = TourFactory(listing=listing1, group=group3)

session.commit()

# TOUR MESSAGES

tm1 = TourMessageFactory(tour=t1, user=user2)
tm2 = TourMessageFactory(tour=t2, user=user3)
tm3 = TourMessageFactory(tour=t3, user=user4)
tm4 = TourMessageFactory(tour=t1, user=landlord1.user)
tm1 = TourMessageFactory(tour=t1, user=user3)
tm1 = TourMessageFactory(tour=t1, user=user4)
tm1 = TourMessageFactory(tour=t1, user=landlord1.user)

session.commit()

# GROUP LISTING
gl1 = GroupListingFactory(group=group1, listing=listing1)
gl2 = GroupListingFactory(group=group1, listing=listing2)
gl3 = GroupListingFactory(group=group1, listing=listing3)

gl1.landlord_show = False
gl2.accepted = True
gl2.completed = True

gl3.accepted = True

session.commit()

# GROUP LISTING MESSAGES
glm1 = GroupListingMessageFactory(groupListing=gl1, user=user2)
glm2 = GroupListingMessageFactory(groupListing=gl1, user=user3)
glm3 = GroupListingMessageFactory(groupListing=gl1, user=user2)
glm4 = GroupListingMessageFactory(groupListing=gl1, user=user5)
glm5 = GroupListingMessageFactory(groupListing=gl1, user=user4)
glm6 = GroupListingMessageFactory(groupListing=gl1, user=user3)
glm7 = GroupListingMessageFactory(groupListing=gl1, user=user2)
glm15 = GroupListingMessageFactory(groupListing=gl1, user=landlord1.user)

glm8 = GroupListingMessageFactory(groupListing=gl2, user=user2)
glm9 = GroupListingMessageFactory(groupListing=gl2, user=user3)
glm10 = GroupListingMessageFactory(groupListing=gl2, user=user2)
glm11 = GroupListingMessageFactory(groupListing=gl2, user=user5)
glm12 = GroupListingMessageFactory(groupListing=gl2, user=user4)
glm13 = GroupListingMessageFactory(groupListing=gl2, user=user3)
glm14 = GroupListingMessageFactory(groupListing=gl2, user=user2)

session.commit()

# SECURITY DEPOSITS FOR GL3
sd1 = SecurityDepositFactory(user=user2, groupListing=gl3)
sd2 = SecurityDepositFactory(user=user3, groupListing=gl3)
sd3 = SecurityDepositFactory(user=user4, groupListing=gl3)
sd4 = SecurityDepositFactory(user=user5, groupListing=gl3)

sd5 = SecurityDepositFactory(user=user2, groupListing=gl2)
sd6 = SecurityDepositFactory(user=user3, groupListing=gl2)
sd7 = SecurityDepositFactory(user=user4, groupListing=gl2)
sd8 = SecurityDepositFactory(user=user5, groupListing=gl2)

sd2.completed = True
sd5.completed = True
sd6.completed = True

session.commit()

