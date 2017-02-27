from nexnest.application import session

from nexnest.data_gen.factories import *

from faker import Faker

fake = Faker()

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

listings = [listing1, listing2, listing3, listing4]


# GROUP USERS
# Group 1
groupuser1 = GroupUserFactory(group=group1, user=user2)
groupuser2 = GroupUserFactory(group=group1, user=user3)
groupuser3 = GroupUserFactory(group=group1, user=user4)
groupuser4 = GroupUserFactory(group=group1, user=user5)

group1Users = [user2, user3, user4, user5]
group1AcceptedUsers = [user2, user3, user4]

# Group 2
groupuser5 = GroupUserFactory(group=group2, user=user3)
groupuser6 = GroupUserFactory(group=group2, user=user2)

group2Users = [user2, user3]

# Group3
groupuser7 = GroupUserFactory(group=group3, user=user2)
groupuser8 = GroupUserFactory(group=group3, user=user8)
groupuser9 = GroupUserFactory(group=group3, user=user3)
groupuser10 = GroupUserFactory(group=group3, user=user4)
groupuser11 = GroupUserFactory(group=group3, user=user5)

group3Users = [user2, user8, user3, user4, user5]

groupuser1.accepted = True
groupuser2.accepted = True
groupuser3.accepted = True
groupuser5.accepted = True
groupuser7.accepted = True


session.commit()

# GROUP LISTING FAVORITES
for listing in listings:
    user = random.choice(group1AcceptedUsers)

    gf = GroupListingFavoriteFactory(group=group1,
                                     listing=listing,
                                     user=user)
    session.commit()

    # for tempUser in group1AcceptedUsers:
    #     if tempUser is not

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
# Group 1

for i in range(10):
    source_user = random.choice(group1AcceptedUsers)

    gmsg = GroupMessageFactory(group=group1, user=source_user)

    session.commit()

    for user in group1AcceptedUsers:
        if user is not source_user:
            gmn = NotificationFactory(target_user=user,
                                      type='group_message',
                                      target_model_id=gmsg.id)
            session.commit()


# DIRECT MESSAGES
# We want MOAR

userMessageList = [user2, user3, user4, user5, landlord, user7, user8]

for i in range(10):
    source_user = random.choice(userMessageList)
    target_user = random.choice(userMessageList)

    while source_user == target_user:
        target_user = random.choice(userMessageList)

    dm = DirectMessageFactory(source_user=source_user, target_user=target_user)

    # Direct Messages Notifications
    dmn = NotificationFactory(target_user=target_user,
                              type='direct_message',
                              target_model_id=source_user.id)
    session.commit()


# TOURS
# Won't show in landlords active tours because listing1 is
# already completed
t1 = TourFactory(listing=listing1, group=group1)
t2 = TourFactory(listing=listing2, group=group2,
                 time_requested=fake.date_time_this_year(before_now=True))
t3 = TourFactory(listing=listing2, group=group3)
t4 = TourFactory(listing=listing3, group=group2)
t5 = TourFactory(listing=listing3, group=group3)
t6 = TourFactory(listing=listing3, group=group1)
t6.tour_confirmed = True

session.commit()

newTourTimeNotif1 = NotificationFactory(target_user=landlord,
                                        type='new_tour_time',
                                        target_model_id=t1.id)
newTourTimeNotif2 = NotificationFactory(target_user=user2,
                                        type='new_tour_time',
                                        target_model_id=t1.id)
session.commit()

# TOUR NOTIFICATIONS
tn1 = NotificationFactory(target_user=landlord,
                          type='tour',
                          target_model_id=t1.id)
tn2 = NotificationFactory(target_user=landlord,
                          type='tour',
                          target_model_id=t2.id)
tn3 = NotificationFactory(target_user=landlord,
                          type='tour',
                          target_model_id=t3.id)
tn4 = NotificationFactory(target_user=landlord,
                          type='tour',
                          target_model_id=t4.id)

session.commit()


# TOUR MESSAGES (t1)
for i in range(5):
    if random.randint(0, 1) == 0:
        tm = TourMessageFactory(tour=t1, user=landlord)
        session.commit()
        for user in group1AcceptedUsers:
            tmn = NotificationFactory(target_user=user,
                                      type='tour_message',
                                      target_model_id=tm.id)
            session.commit()
    else:
        user = random.choice(group1AcceptedUsers)

        tm = TourMessageFactory(tour=t1, user=user)

        session.commit()

        for tempUser in group1AcceptedUsers:
            if tempUser is not user:
                tmn = NotificationFactory(target_user=tempUser,
                                          type='tour_message',
                                          target_model_id=tm.id)
                session.commit()

        tmn = NotificationFactory(target_user=landlord,
                                  type='tour_message',
                                  target_model_id=tm.id)
        session.commit()


# GROUP LISTING
gl1 = GroupListingFactory(group=group1, listing=listing1)
gl2 = GroupListingFactory(group=group1, listing=listing2)
gl3 = GroupListingFactory(group=group1, listing=listing3)

gl1.accepted = True
gl1.completed = True

gl3.accepted = True

session.commit()

# GROUP LISTING MESSAGES
for i in range(10):
    userTemp = random.choice(group1AcceptedUsers)
    glm = GroupListingMessageFactory(groupListing=gl1, user=userTemp)

    session.commit()

    for user in group1AcceptedUsers:
        if user is not userTemp:
            glmn = NotificationFactory(target_user=user,
                                       type='group_listing_message',
                                       target_model_id=glm.id)
            session.commit()

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
# gl1 (group 1)
for user in group1AcceptedUsers:
    sd = SecurityDepositFactory(user=user, groupListing=gl1)

    if random.randint(0, 1) == 0:
        sd.completed = True
        session.commit()

        sdn = NotificationFactory(target_user=landlord,
                                  type='security_deposit',
                                  target_model_id=sd.id)
    session.commit()


# House
h1 = HouseFactory(listing=listing1, group=group1)

session.commit()

for user in group1AcceptedUsers:
    hnf = NotificationFactory(target_user=user,
                              type='house',
                              target_model_id=h1.id)

# House Messages
for i in range(3):
    user = random.choice(group1AcceptedUsers)

    hm = HouseMessageFactory(house=h1, user=user)

    session.commit()

    for userTemp in group1AcceptedUsers:
        if userTemp is not user:
            hmn = NotificationFactory(target_user=userTemp,
                                      type='house_message',
                                      target_model_id=hm.id)
            session.commit()

# -- House Messages (Landlord)
hm = HouseMessageFactory(house=h1, user=landlord)

session.commit()

for user in group1AcceptedUsers:
    hmn = NotificationFactory(target_user=user,
                              type='house_message',
                              target_model_id=hm.id)
    session.commit()


# Maintenance Requests
m1 = MaintenanceFactory(house=h1, user=user2)
m2 = MaintenanceFactory(house=h1, user=user3)
m3 = MaintenanceFactory(house=h1, user=user4)

m2.status = 'inprogress'
m3.status = 'completed'

session.commit()

mn1 = NotificationFactory(target_user=landlord,
                          type='maintenance',
                          target_model_id=m1.id)
mn2 = NotificationFactory(target_user=landlord,
                          type='maintenance',
                          target_model_id=m2.id)
mn3 = NotificationFactory(target_user=landlord,
                          type='maintenance',
                          target_model_id=m3.id)
session.commit()

# Maintenance Request Messages

# m1
for i in range(5):
    user = random.choice(group1AcceptedUsers)

    mm = MaintenanceMessageFactory(maintenance=m1, user=user)

    session.commit()

    for tempUser in group1AcceptedUsers:
        if tempUser is not user:
            mmn = NotificationFactory(target_user=tempUser,
                                      type='maintenance_message',
                                      target_model_id=mm.id)
            session.commit()
    mmn = NotificationFactory(target_user=landlord,
                              type='maintenance_message',
                              target_model_id=mm.id)
    session.commit()

# m2
mm5 = MaintenanceMessageFactory(maintenance=m2, user=user5)
mm6 = MaintenanceMessageFactory(maintenance=m2, user=user2)
mm7 = MaintenanceMessageFactory(maintenance=m2, user=user3)

# m3
mm8 = MaintenanceMessageFactory(maintenance=m3, user=user2)
mm9 = MaintenanceMessageFactory(maintenance=m3, user=user3)
mm10 = MaintenanceMessageFactory(maintenance=m3, user=user4)

session.commit()
