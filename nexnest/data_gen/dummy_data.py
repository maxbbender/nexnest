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
# group 4
user9 = UserFactory(school=s)
user10 = UserFactory(school=s)
user11 = UserFactory(school=s)
user12 = UserFactory(school=s)
# group 5
user13 = UserFactory(school=s)
user14 = UserFactory(school=s)
user15 = UserFactory(school=s)
# group 6
user16 = UserFactory(school=s)
user17 = UserFactory(school=s)
user18 = UserFactory(school=s)
# group 7
user19 = UserFactory(school=s)
user20 = UserFactory(school=s)
user21 = UserFactory(school=s)
user22 = UserFactory(school=s)
user23 = UserFactory(school=s)

admin = UserFactory(role='admin', email='admin@admin.com')

session.commit()

# LANDLORDS
landlord1 = LandlordFactory(user=landlord)

session.commit()

# LISTINGS
start_date = fake.date_time_this_year(before_now=True)
end_date = fake.date_time_this_year(before_now=False, after_now=True)
listing1 = ListingFactory(start_date=start_date, end_date=end_date, num_bedrooms=4)
listing2 = ListingFactory(start_date=fake.date_time_this_year(before_now=False, after_now=True))
listing3 = ListingFactory()
listing4 = ListingFactory()
listing5 = ListingFactory()
listing6 = ListingFactory()

session.commit()

# LANDLORD LISTINGS
landlordListing1 = LandlordListingFactory(landlord=landlord1, listing=listing1)
landlordListing2 = LandlordListingFactory(landlord=landlord1, listing=listing2)
landlordListing3 = LandlordListingFactory(landlord=landlord1, listing=listing3)
landlordListing4 = LandlordListingFactory(landlord=landlord1, listing=listing4)
landlordListing5 = LandlordListingFactory(landlord=landlord1, listing=listing5)
landlordListing6 = LandlordListingFactory(landlord=landlord1, listing=listing6)

session.commit()

# GROUP
group1 = GroupFactory(leader=user2)
group2 = GroupFactory(leader=user3)
group3 = GroupFactory(leader=user4)


group4 = GroupFactory(leader=user9)
group5 = GroupFactory(leader=user13)
group6 = GroupFactory(leader=user16)
group7 = GroupFactory(leader=user19)

session.commit()

listings = [listing1, listing2, listing3, listing4, listing5, listing6]


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

# group 4
groupuser12 = GroupUserFactory(group=group4, user=user9)
groupuser13 = GroupUserFactory(group=group4, user=user10)
groupuser14 = GroupUserFactory(group=group4, user=user11)
groupuser15 = GroupUserFactory(group=group4, user=user12)

group4Users = [user9, user10, user11, user12]
group4AcceptedUsers = [user9, user10, user11, user12]

# group 5
groupuser16 = GroupUserFactory(group=group5, user=user13)
groupuser17 = GroupUserFactory(group=group5, user=user14)
groupuser18 = GroupUserFactory(group=group5, user=user15)

group5Users = [user13, user14, user15]
group5AcceptedUsers = [user13, user14, user15]

# group 6
groupuser19 = GroupUserFactory(group=group6, user=user16)
groupuser20 = GroupUserFactory(group=group6, user=user17)
groupuser21 = GroupUserFactory(group=group6, user=user18)

group6Users = [user16, user17, user18]
group6AcceptedUsers = [user16, user17, user18]

# group 7
groupuser22 = GroupUserFactory(group=group7, user=user19)
groupuser23 = GroupUserFactory(group=group7, user=user20)
groupuser24 = GroupUserFactory(group=group7, user=user21)
groupuser25 = GroupUserFactory(group=group7, user=user22)
groupuser26 = GroupUserFactory(group=group7, user=user23)

group7Users = [user19, user20, user21, user22, user23]
group7AcceptedUsers = [user19, user20, user21, user22, user23]

groupuser1.accepted = True
groupuser2.accepted = True
groupuser3.accepted = True
groupuser5.accepted = True
groupuser7.accepted = True

groupuser12.accepted = True
groupuser13.accepted = True
groupuser14.accepted = True
groupuser15.accepted = True
groupuser16.accepted = True
groupuser17.accepted = True
groupuser18.accepted = True
groupuser19.accepted = True
groupuser20.accepted = True
groupuser21.accepted = True
groupuser22.accepted = True
groupuser23.accepted = True
groupuser24.accepted = True
groupuser25.accepted = True
groupuser26.accepted = True


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
                            notif_type='group_listing_favorite',
                            target_model_id=group1.id)
glfn2 = NotificationFactory(target_user=user4,
                            notif_type='group_listing_favorite',
                            target_model_id=group1.id)
glfn3 = NotificationFactory(target_user=user5,
                            notif_type='group_listing_favorite',
                            target_model_id=group1.id)
glfn4 = NotificationFactory(target_user=user3,
                            notif_type='group_listing_favorite',
                            target_model_id=group1.id)
glfn5 = NotificationFactory(target_user=user6,
                            notif_type='group_listing_favorite',
                            target_model_id=group2.id)
glfn6 = NotificationFactory(target_user=user8,
                            notif_type='group_listing_favorite',
                            target_model_id=group3.id)


# GROUP USER NOTIFICATIONS
gun1 = NotificationFactory(target_user=groupuser4.user,
                           notif_type='group_user',
                           target_model_id=groupuser4.group.id)
gun2 = NotificationFactory(target_user=groupuser5.user,
                           notif_type='group_user',
                           target_model_id=groupuser5.group.id)
gun3 = NotificationFactory(target_user=groupuser8.user,
                           notif_type='group_user',
                           target_model_id=groupuser8.group.id)
gun4 = NotificationFactory(target_user=groupuser9.user,
                           notif_type='group_user',
                           target_model_id=groupuser9.group.id)
gun5 = NotificationFactory(target_user=groupuser10.user,
                           notif_type='group_user',
                           target_model_id=groupuser10.group.id)
gun6 = NotificationFactory(target_user=groupuser11.user,
                           notif_type='group_user',
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
                                      notif_type='group_message',
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
                              notif_type='direct_message',
                              target_model_id=source_user.id)
    session.commit()


# TOURS
# Won't show in landlords active tours because listing1 is
# already completed
t1 = TourFactory(listing=listing1, group=group4)
t2 = TourFactory(listing=listing2, group=group4,
                 time_requested=fake.date_time_this_year(before_now=True))
t3 = TourFactory(listing=listing2, group=group5)
t4 = TourFactory(listing=listing4, group=group5)
t5 = TourFactory(listing=listing5, group=group6)
t6 = TourFactory(listing=listing5, group=group7)

session.commit()

newTourTimeNotif1 = NotificationFactory(target_user=landlord,
                                        notif_type='new_tour_time',
                                        target_model_id=t1.id)
newTourTimeNotif2 = NotificationFactory(target_user=user2,
                                        notif_type='new_tour_time',
                                        target_model_id=t1.id)
session.commit()

# TOUR NOTIFICATIONS
tn1 = NotificationFactory(target_user=landlord,
                          notif_type='tour',
                          target_model_id=t1.id)
tn2 = NotificationFactory(target_user=landlord,
                          notif_type='tour',
                          target_model_id=t2.id)
tn3 = NotificationFactory(target_user=landlord,
                          notif_type='tour',
                          target_model_id=t3.id)
tn4 = NotificationFactory(target_user=landlord,
                          notif_type='tour',
                          target_model_id=t4.id)

session.commit()


# TOUR MESSAGES (t1)
for i in range(5):
    if random.randint(0, 1) == 0:
        tm = TourMessageFactory(tour=t1, user=landlord)
        session.commit()
        for user in group1AcceptedUsers:
            tmn = NotificationFactory(target_user=user,
                                      notif_type='tour_message',
                                      target_model_id=tm.id)
            session.commit()
    else:
        user = random.choice(group1AcceptedUsers)

        tm = TourMessageFactory(tour=t1, user=user)

        session.commit()

        for tempUser in group1AcceptedUsers:
            if tempUser is not user:
                tmn = NotificationFactory(target_user=tempUser,
                                          notif_type='tour_message',
                                          target_model_id=tm.id)
                session.commit()

        tmn = NotificationFactory(target_user=landlord,
                                  notif_type='tour_message',
                                  target_model_id=tm.id)
        session.commit()


# GROUP LISTING
gl1 = GroupListingFactory(group=group1, listing=listing1)
gl2 = GroupListingFactory(group=group2, listing=listing2)
gl3 = GroupListingFactory(group=group3, listing=listing3)

gl4 = GroupListingFactory(group=group4, listing=listing4)
gl5 = GroupListingFactory(group=group5, listing=listing2)
gl6 = GroupListingFactory(group=group6, listing=listing5)
gl7 = GroupListingFactory(group=group7, listing=listing6)

gl1.accepted = True
gl7.accepted = True

session.commit()

# GROUP LISTING MESSAGES
for i in range(10):
    userTemp = random.choice(group1AcceptedUsers)
    glm = GroupListingMessageFactory(groupListing=gl1, user=userTemp)

    session.commit()

    for user in group1AcceptedUsers:
        if user is not userTemp:
            glmn = NotificationFactory(target_user=user,
                                       notif_type='group_listing_message',
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
                                  notif_type='security_deposit',
                                  target_model_id=sd.id)
    session.commit()

# gl7 (group 7)
for user in group7AcceptedUsers:
    sd = SecurityDepositFactory(user=user, groupListing=gl7)

    if random.randint(0, 1) == 0:
        sd.completed = True
        session.commit()

        sdn = NotificationFactory(target_user=landlord,
                                  notif_type='security_deposit',
                                  target_model_id=sd.id)
    session.commit()


# House
h1 = HouseFactory(listing=listing1, group=group1)
h2 = HouseFactory(listing=listing2, group=group2)

session.commit()

for user in group1AcceptedUsers:
    hnf = NotificationFactory(target_user=user,
                              notif_type='house',
                              target_model_id=h1.id)

# House Messages
for i in range(3):
    user = random.choice(group1AcceptedUsers)

    hm = HouseMessageFactory(house=h1, user=user)

    session.commit()

    for userTemp in group1AcceptedUsers:
        if userTemp is not user:
            hmn = NotificationFactory(target_user=userTemp,
                                      notif_type='house_message',
                                      target_model_id=hm.id)
            session.commit()

# -- House Messages (Landlord)
hm = HouseMessageFactory(house=h1, user=landlord)

session.commit()

for user in group1AcceptedUsers:
    hmn = NotificationFactory(target_user=user,
                              notif_type='house_message',
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
                          notif_type='maintenance',
                          target_model_id=m1.id)
mn2 = NotificationFactory(target_user=landlord,
                          notif_type='maintenance',
                          target_model_id=m2.id)
mn3 = NotificationFactory(target_user=landlord,
                          notif_type='maintenance',
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
                                      notif_type='maintenance_message',
                                      target_model_id=mm.id)
            session.commit()
    mmn = NotificationFactory(target_user=landlord,
                              notif_type='maintenance_message',
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
