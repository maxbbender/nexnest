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

# GROUP LISTING FAVORITES
gf1 = GroupListingFavoriteFactory(group=group1,
                                  listing=listing1,
                                  user=user2)
gf2 = GroupListingFavoriteFactory(group=group2,
                                  listing=listing1,
                                  user=user5)
gf3 = GroupListingFavoriteFactory(group=group3,
                                  listing=listing1,
                                  user=user7)
gf4 = GroupListingFavoriteFactory(group=group2,
                                  listing=listing3,
                                  user=user6)
gf5 = GroupListingFavoriteFactory(group=group1,
                                  listing=listing2,
                                  user=user3)

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
groupuser6.accepted = True
groupuser7.accepted = True


session.commit()

# GROUP FAVORITE NOTIFICATIONS
glfn1 = NotificationFactory(target_user=user3,
                            type='group_listing_favorite',
                            target_model_id=group1.id)
glfn2 = NotificationFactory(target_user=user4,
                            type='group_listing_favorite',
                            target_model_id=group1.id)
glfn3 = NotificationFactory(target_user=user5,
                            type='group_listing_favorite',
                            target_model_id=group1.id)
glfn4 = NotificationFactory(target_user=user3,
                            type='group_listing_favorite',
                            target_model_id=group1.id)
glfn5 = NotificationFactory(target_user=user6,
                            type='group_listing_favorite',
                            target_model_id=group2.id)
glfn6 = NotificationFactory(target_user=user8,
                            type='group_listing_favorite',
                            target_model_id=group3.id)


# GROUP USER NOTIFICATIONS
gun1 = NotificationFactory(target_user=groupuser4.user,
                           type='group_user',
                           target_model_id=groupuser4.group.id)
gun2 = NotificationFactory(target_user=groupuser5.user,
                           type='group_user',
                           target_model_id=groupuser5.group.id)
gun3 = NotificationFactory(target_user=groupuser8.user,
                           type='group_user',
                           target_model_id=groupuser8.group.id)
gun4 = NotificationFactory(target_user=groupuser9.user,
                           type='group_user',
                           target_model_id=groupuser9.group.id)
gun5 = NotificationFactory(target_user=groupuser10.user,
                           type='group_user',
                           target_model_id=groupuser10.group.id)
gun6 = NotificationFactory(target_user=groupuser11.user,
                           type='group_user',
                           target_model_id=groupuser11.group.id)

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
# We want MOAR

userMessageList = [user2, user3, user4, user5, landlord, user7, user8]

for i in range(50):
    source_user = random.choice(userMessageList)
    target_user = random.choice(userMessageList)

    while source_user == target_user:
        target_user = random.choice(userMessageList)

    dm = DirectMessageFactory(source_user=source_user, target_user=target_user)

    #_Direct Messages Notifications
    dmn = NotificationFactory(target_user=target_user,
                              type='direct_message',
                              target_model_id=source_user.id)
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

#gl1.landlord_show = False
gl2.accepted = True
gl2.completed = True

gl3.accepted = True

session.commit()

# GROUP LISTING MESSAGES
# # GL1
# gl1Users = [user2, user3, user4, user5]
# for i in range(30):
#     userTemp = random.choice(gl1Users)
#     glm = GroupListingMessageFactory(groupListing=gl1, user=userTemp)

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

# SECURITY DEPOSITS

# gl3
sd1 = SecurityDepositFactory(user=user2, groupListing=gl3)
sd2 = SecurityDepositFactory(user=user3, groupListing=gl3)
sd3 = SecurityDepositFactory(user=user4, groupListing=gl3)
sd4 = SecurityDepositFactory(user=user5, groupListing=gl3)

# gl2
sd5 = SecurityDepositFactory(user=user2, groupListing=gl2)
sd6 = SecurityDepositFactory(user=user3, groupListing=gl2)
sd7 = SecurityDepositFactory(user=user4, groupListing=gl2)
sd8 = SecurityDepositFactory(user=user5, groupListing=gl2)

sd2.completed = True
sd5.completed = True
sd6.completed = True

session.commit()

# House
h1 = HouseFactory(listing=listing2, group=group1)

session.commit()

# House Messages
hm1 = HouseMessageFactory(house=h1, user=user2)
hm2 = HouseMessageFactory(house=h1, user=user3)
hm3 = HouseMessageFactory(house=h1, user=user2)
hm4 = HouseMessageFactory(house=h1, user=user5)
hm5 = HouseMessageFactory(house=h1, user=landlord1.user)

# Maintenance Requests
m1 = MaintenanceFactory(house=h1, user=user2)
m2 = MaintenanceFactory(house=h1, user=user3)
m3 = MaintenanceFactory(house=h1, user=user4)

m2.status = 'inprogress'
m3.status = 'completed'

session.commit()

# Maintenance Request Messages

# m1
mm1 = MaintenanceMessageFactory(maintenance=m1, user=user2)
mm2 = MaintenanceMessageFactory(maintenance=m1, user=user3)
mm3 = MaintenanceMessageFactory(maintenance=m1, user=user2)
mm4 = MaintenanceMessageFactory(maintenance=m1, user=user4)

# m2
mm5 = MaintenanceMessageFactory(maintenance=m2, user=user5)
mm6 = MaintenanceMessageFactory(maintenance=m2, user=user2)
mm7 = MaintenanceMessageFactory(maintenance=m2, user=user3)

# m3
mm8 = MaintenanceMessageFactory(maintenance=m3, user=user2)
mm9 = MaintenanceMessageFactory(maintenance=m3, user=user3)
mm10 = MaintenanceMessageFactory(maintenance=m3, user=user4)

session.commit()


# Notifications
