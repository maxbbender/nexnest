import json
import os
from pprint import pformat

import requests
from dateutil import parser
from flask import current_app as app
from flask import (Blueprint, abort, flash, jsonify, redirect, render_template,
                   request, url_for)
from flask_login import current_user, login_required, login_user, logout_user
from itsdangerous import BadSignature
from nexnest import csrf, db
from nexnest.decorators import user_editable
from nexnest.forms import (CreateGroupForm, DirectMessageForm, EditAccountForm,
                           EmailPreferencesForm, LandlordEditAccountForm,
                           LandlordMoreInfoForm, LoginForm, NewPasswordForm,
                           PasswordChangeForm, ProfilePictureForm,
                           RegistrationForm)
from nexnest.models.availability import Availability
from nexnest.models.direct_message import DirectMessage
from nexnest.models.group import Group
from nexnest.models.group_email import GroupEmail
from nexnest.models.group_user import GroupUser
from nexnest.models.landlord import Landlord
from nexnest.models.listing import Listing
from nexnest.models.listing_favorite import ListingFavorite
from nexnest.models.notification import Notification
from nexnest.models.notification_preference import NotificationPreference
from nexnest.models.school import School
from nexnest.models.user import User
from nexnest.utils.email import confirm_token, generate_confirmation_token
from nexnest.utils.file import allowed_file
from nexnest.utils.flash import flash_errors
from nexnest.utils.password import check_password
from nexnest.utils.school import allSchoolsAsStrings
from nexnest.utils.user import (genEmailPasswordResetContent,
                                genEmailVerificationContent)
from sqlalchemy import and_, asc, desc, func, or_
from werkzeug.utils import secure_filename

users = Blueprint('users', __name__, template_folder='../templates/user')

session = db.session


@users.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        if current_user.is_authenticated:
            return redirect(url_for('indexs.index'))

        return render_template('register.html',
                               form=RegistrationForm(),
                               schools=allSchoolsAsStrings())
    else:
        registerForm = RegistrationForm(request.form)

        if registerForm.validate():
            # Determine if registering as tenant or landlord
            userType = registerForm.landlord.data
            app.logger.debug('Verifying Captcha')
            captchaConfirmURL = 'https://www.google.com/recaptcha/api/siteverify'
            payload = {'response': request.form['g-recaptcha-response'],
                       'secret': app.config['GOOGLE_CAPTCHA_SECRET']}

            response = requests.post(captchaConfirmURL, data=payload)

            responseObject = json.loads(response.text)

            app.logger.debug('Response Text %s' % response.text)
            app.logger.debug('Response Dict %r' % pformat(responseObject))

            if responseObject['success']:
                if userType == "landlord":
                    newUser = User(email=registerForm.email.data,
                                   password=registerForm.password.data,
                                   fname=registerForm.fname.data,
                                   lname=registerForm.lname.data,
                                   landlord_info_filled=False)
                    session.add(newUser)
                    session.commit()

                    # Make them a Landlord

                    # Notification Preference Table init
                    session.add(NotificationPreference(
                        user=newUser, newsletter=registerForm.newsletter.data))
                    session.commit()

                    newLandlord = Landlord(newUser)
                    session.add(newLandlord)
                    session.commit()

                else:
                    school = session.query(School) \
                        .filter(func.lower(School.name) == registerForm.school.data.lower()) \
                        .first()

                    if school is not None:
                        # School Exists
                        newUser = User(email=registerForm.email.data,
                                       password=registerForm.password.data,
                                       fname=registerForm.fname.data,
                                       lname=registerForm.lname.data,
                                       school=school)
                        session.add(newUser)
                        session.commit()

                        # Notification Preference Table init
                        session.add(NotificationPreference(
                            user=newUser, newsletter=registerForm.newsletter.data))
                        session.commit()

                        # emailConfirmURL = url_for('users.emailConfirm', payload=generate_confirmation_token(newUser.email), _external=True)
                        # newUser.sendEmail('generic',
                        #                   'Click the link to confirm your account <a href="%s">Click Here</a>' % emailConfirmURL)

                emailConfirmURL = url_for('users.emailConfirm', payload=generate_confirmation_token(
                    newUser.email), _external=True)
                newUser.sendEmail('emailVerification',
                                  genEmailVerificationContent(newUser, emailConfirmURL))

                return redirect(url_for('users.emailConfirmNotice', email=registerForm.email.data))
            else:
                flash('Captcha Error: Codes %r' %
                      responseObject['error-codes'], 'danger')
                return render_template('register.html', form=registerForm, schools=allSchoolsAsStrings())

        flash_errors(registerForm)
        return render_template('register.html', form=registerForm, schools=allSchoolsAsStrings())


# BRAINTREE UPDATE
@users.route('/register/landlordInformation', methods=['GET', 'POST'])
@login_required
@user_editable
def landlordInformation():
    landlord = Landlord.query.filter_by(user=current_user).first_or_404()

    if request.method == 'GET':
        return render_template('landlordMoreInformation.html',
                               form=LandlordMoreInfoForm(obj=landlord))
    else:  # Post
        moreInformationForm = LandlordMoreInfoForm(request.form)

        if moreInformationForm.validate():
            landlord.street = moreInformationForm.street.data
            landlord.city = moreInformationForm.city.data
            landlord.state = moreInformationForm.state.data
            landlord.zip_code = moreInformationForm.zip_code.data
            landlord.check_pay = moreInformationForm.check_pay.data
            landlord.online_pay = moreInformationForm.online_pay.data
            landlord.user.dob = moreInformationForm.date_of_birth.data
            landlord.user.phone = moreInformationForm.phone.data
            landlord.user.landlord_info_filled = True

            session.commit()

            availabilityJSON = json.loads(
                moreInformationForm.availabilities.data)
            app.logger.debug('availabilityJSON %r' % availabilityJSON)

            for i in range(7):
                day = str(i)
                if day in availabilityJSON:
                    if len(availabilityJSON[day]) > 0:
                        for time in availabilityJSON[day]:
                            time = parser.parse(time).time()
                            newAvailability = Availability(landlord, time, day)
                            session.add(newAvailability)
                            session.commit()

            flash('Your Information was successfully saved!', 'success')
            return redirect(url_for('landlords.landlordDashboard'))
            # return moreInformationForm.redirect()

        flash_errors(moreInformationForm)
        return render_template('/landlordMoreInformation.html', form=moreInformationForm, userID=landlord.user.id)


@users.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        loginForm = LoginForm()
        if request.args.get('next') is not None:
            loginForm.nextURL.data = request.args['next']

        return render_template('login.html', login_form=loginForm)
    else:  # POST
        login_form = LoginForm(request.form)

        if login_form.validate():

            user = session.query(User) \
                .filter_by(email=login_form.email.data) \
                .first()

            # Does the user exist
            if user is not None:
                if user.active:
                    if check_password(user, login_form.password.data):
                        if user.email_confirmed:
                            login_user(user)

                            # See if they have any pending group email invites
                            groupEmailInvites = GroupEmail.query.filter_by(
                                email=user.email, used=False).all()

                            if len(groupEmailInvites) > 0:
                                for groupEmail in groupEmailInvites:
                                    groupUserCheck = GroupUser.query.filter_by(
                                        group=groupEmail.group, user=user).count()
                                    errorMessage = None
                                    if groupUserCheck == 0:
                                        newGroupUser = GroupUser(
                                            groupEmail.group, user)
                                        newGroupUser.accepted = True
                                        groupEmail.used = True
                                        session.add(newGroupUser)
                                        session.commit()
                                    else:
                                        groupEmail.used = True
                                        session.commit()

                        else:
                            flash(
                                'You must confirm your email before logging in', 'danger')
                    else:
                        flash("Error validating login credentials", 'danger')
                        return login_form.redirect()
                else:
                    flash("User account has been deleted", 'warning')
            else:
                flash("There was no account found with an email address matching %s" %
                      login_form.email.data, 'warning')
        else:
            flash_errors(login_form)

        if user is not None:
            if user.isLandlord:
                if user.landlord_info_filled:
                    return redirect('/landlord/dashboard')
                else:
                    return redirect(url_for('users.landlordInformation'))

        return login_form.redirect()


@users.route('/logout')
def logout():
    logout_user()
    return redirect("/")


@users.route('/emailConfirm/<email>')
def emailConfirmNotice(email):
    return render_template('/user/confirmEmail.html',
                           email=email)


@users.route('/user/emailConfirm/<payload>')
def emailConfirm(payload):
    try:
        email = confirm_token(payload)
    except:
        flash('The confirmation link is invalid or has expired.', 'danger')
    user = User.query.filter_by(email=email).first_or_404()

    if user.email_confirmed:
        flash('Account already confirmed. Please login.', 'success')
    else:
        user.email_confirmed = True
        session.commit()
        flash('You have confirmed your account, you can now sign in!', 'success')

    return redirect(url_for('indexs.index'))


@users.route('/user/view/<userID>', methods=['GET', 'POST'])
@login_required
def viewUser(userID):
    # fake lisiting for testing
    if current_user.id == int(userID):

        form = EmailPreferencesForm(request.form)
        user = session.query(User).filter_by(id=userID).first()
        currentPreferences = session.query(
            NotificationPreference).filter_by(user_id=userID).first()
        userFavorites = session.query(
            ListingFavorite).filter_by(user=current_user).all()
        myGroups = current_user.accepted_groups
        app.logger.debug(currentPreferences)
        form = EmailPreferencesForm(obj=currentPreferences)

        if request.method == 'GET':
            return render_template('/user/account.html',
                                   user=user,
                                   form=form,
                                   title=user.fname,
                                   userFavorites=userFavorites,
                                   groups=myGroups
                                   )

        else:
            if form.validate():
                currentPreferences.direct_message_email = form.direct_message_email.data
                currentPreferences.tour_message_email = form.tour_message_email.data
                currentPreferences.group_message_email = form.group_message_email.data
                currentPreferences.house_message_email = form.house_message_email.data
                currentPreferences.maintenance_message_email = form.maintenance_message_email.data
                currentPreferences.tour_time_email = form.tour_time_email.data
                currentPreferences.tour_confirmed_email = form.tour_confirmed_email.data
                currentPreferences.tour_denied_email = form.tour_denied_email.data
                currentPreferences.maintenance_email = form.maintenance_email.data
                currentPreferences.maintenance_inProgress_email = form.maintenance_inProgress_email.data
                currentPreferences.maintenance_completed_email = form.maintenance_completed_email.data
                currentPreferences.rent_due_email = form.rent_due_email.data
                currentPreferences.rent_paid_email = form.rent_paid_email.data
                currentPreferences.group_user_email = form.group_user_email.data
                currentPreferences.group_listing_email = form.group_listing_email.data
                currentPreferences.group_listing_accept_email = form.group_listing_accept_email.data
                currentPreferences.group_listing_deny_email = form.group_listing_deny_email.data
                currentPreferences.direct_message_notification = form.direct_message_notification.data
                currentPreferences.tour_message_notification = form.tour_message_notification.data
                currentPreferences.group_message_notification = form.group_message_notification.data
                currentPreferences.house_message_notification = form.house_message_notification.data
                currentPreferences.maintenance_message_notification = form.maintenance_message_notification.data
                currentPreferences.tour_time_notification = form.tour_time_notification.data
                currentPreferences.tour_confirmed_notification = form.tour_confirmed_notification.data
                currentPreferences.tour_denied_notification = form.tour_denied_notification.data
                currentPreferences.maintenance_notification = form.maintenance_notification.data
                currentPreferences.maintenance_inProgress_notification = form.maintenance_inProgress_notification.data
                currentPreferences.maintenance_completed_notification = form.maintenance_completed_notification.data
                currentPreferences.rent_due_notification = form.rent_due_notification.data
                currentPreferences.rent_paid_notification = form.rent_paid_notification.data
                currentPreferences.group_user_notification = form.group_user_notification.data
                currentPreferences.group_listing_notification = form.group_listing_notification.data
                currentPreferences.group_listing_accept_notification = form.group_listing_accept_notification.data
                currentPreferences.group_listing_deny_notification = form.group_listing_deny_notification.data
                currentPreferences.newsletter_email = form.newsletter_email.data
                session.commit()

                flash('Preferences Updated', 'success')
                return render_template('/user/account.html',
                                       user=user,
                                       form=form,
                                       title=user.fname
                                       )
            else:
                flash_errors(form)
                return redirect(url_for('users.viewUser',
                                        userID=userID))
    else:
        app.logger.warning('User %r attempted to access user_ids page %s' %
                           (current_user, userID))
        abort(404)


@users.route('/user/edit/info', methods=['GET', 'POST'])
@login_required
@user_editable
def editAccountInfo():
    landlord = None
    currentUserIsLandlord = current_user.isLandlord
    if currentUserIsLandlord:
        landlord = Landlord.query.filter_by(user=current_user).first()
        form = LandlordEditAccountForm(request.form)
    else:
        form = EditAccountForm(request.form)

    if form.validate_on_submit():
        flash('Successfully updated your account', 'success')
        current_user.fname = form.fname.data
        current_user.lname = form.lname.data
        current_user.email = form.email.data

        if currentUserIsLandlord:
            landlord.online_pay = form.online_pay.data
            landlord.check_pay = form.check_pay.data
            landlord.street = form.street.data
            landlord.city = form.city.data
            landlord.zip_code = form.zip_code.data
            landlord.state = form.state.data
            if form.date_of_birth.data != '':
                current_user.dob = form.date_of_birth.data
            current_user.phone = form.phone.data

        else:
            if form.school.data != current_user.school.name:
                school = School.query.filter_by(name=form.school.data).first()

                if school is not None:
                    current_user.school_id = school.id

        session.commit()

        return redirect(url_for('users.viewUser', userID=current_user.id))
    else:
        flash_errors(form)

    if currentUserIsLandlord:
        form = LandlordEditAccountForm(request.form, obj=landlord)

        form.fname.data = current_user.fname
        form.lname.data = current_user.lname
        form.date_of_birth.data = current_user.dob
        form.phone.data = current_user.phone
        form.email.data = current_user.email

        return render_template('editAccount.html',
                               form=form,
                               title='Edit Account',
                               schools=None,
                               dob=current_user.dob)
    else:
        schools = [r for r, in session.query(School.name).all()]
        form = EditAccountForm(request.form, obj=current_user)

        if current_user.school:
            form.school.data = current_user.school.name
        return render_template('editAccount.html',
                               form=form,
                               title='Edit Account',
                               schools=schools)


@users.route('/user/search/<username>')
@login_required
def searchForUser(username):
    usersToReturn = session.query(User).filter(func.lower(
        User.username).like(func.lower(username + "%"))).all()

    return jsonify(users=[i.serialize for i in usersToReturn])


@users.route('/user/acceptGroupInvite/<groupID>')
@login_required
def acceptGroupInvite(groupID):
    group = session.query(Group).filter_by(id=groupID).first()
    current_user.accept_group_invite(group)
    return redirect(url_for('groups.viewGroup', groupID=group.id))


@users.route('/user/declineGroupInvite/<groupID>')
@login_required
def declineGroupInvite(groupID):
    group = session.query(Group).filter_by(id=groupID).first()
    current_user.decline_group_invite(group)

    if request.is_xhr:
        return jsonify({'success': True})
    else:
        return redirect(url_for('users.myGroups'))


@users.route('/user/search/<username>/<group_id>')
@login_required
def searchForGroupUser(username, group_id):
    usersToReturn = session.query(User).filter(func.lower(
        User.username).like(func.lower(username + "%"))).all()

    group = session.query(Group).filter_by(id=group_id).first()

    userList = []
    apartOfGroup = False
    for user in usersToReturn:
        if user.isLandlord:
            continue

        for groupUser in user.groups:
            if groupUser.group == group:
                apartOfGroup = True
                break
        if not apartOfGroup:
            userList.append(user.serialize)
        else:
            apartOfGroup = False

    return jsonify(users=userList)


@users.route('/user/directMessages')
@login_required
def directMessagesAll():
    allMessages = []

    sentDirectMessages = DirectMessage.query.filter_by(user=current_user) \
        .distinct(DirectMessage.target_user_id) \
        .order_by(DirectMessage.target_user_id, desc(DirectMessage.date_created)) \
        .all()

    app.logger.debug('sentDirectMessages %r' % sentDirectMessages)

    allMessages = sentDirectMessages

    recievedDirectMessages = DirectMessage.query.filter_by(target_user_id=current_user.id) \
        .distinct(DirectMessage.user_id) \
        .order_by(DirectMessage.user_id, desc(DirectMessage.date_created)) \
        .all()

    messageUserIDList = []

    for message in sentDirectMessages:
        messageUserIDList.append(message.target_user_id)

    for message in recievedDirectMessages:
        if message.user_id not in messageUserIDList:
            allMessages.append(message)
        else:
            messageToCheck = None

            # Check to see if recieved message was sooner than sent
            for idx, sentMessage in enumerate(allMessages):
                if message.user_id == sentMessage.target_user_id:
                    if message.date_created > sentMessage.date_created:
                        allMessages.remove(sentMessage)
                        allMessages.insert(idx, message)
                    break

    app.logger.debug('allMessages %r' % allMessages)

    return render_template('directMessageAll.html',
                           directMessages=allMessages)


@users.route('/user/directMessages/<userID>')
@login_required
def directMessagesIndividual(userID):
    targetUser = User.query.filter_by(id=userID).first_or_404()

    form = DirectMessageForm()

    allMessages = DirectMessage.query \
        .filter(or_(and_(DirectMessage.user_id == current_user.id,
                         DirectMessage.target_user_id == targetUser.id),
                    and_(DirectMessage.user_id == targetUser.id,
                         DirectMessage.target_user_id == current_user.id))) \
        .order_by(desc(DirectMessage.date_created)) \
        .all()

    app.logger.debug('allMessages %r' % allMessages)

    return render_template('directMessageIndividual.html',
                           targetUser=targetUser,
                           messages=allMessages,
                           form=form)


@users.route('/user/directMessages/create', methods=['POST'])
@login_required
def createDirectMessage():
    dmForm = DirectMessageForm(request.form)

    if dmForm.validate():
        target_user = session.query(User) \
            .filter_by(id=dmForm.target_user_id.data) \
            .first()

        newDM = DirectMessage(current_user, target_user, dmForm.content.data)
        session.add(newDM)
        session.commit()

        newDM.genNotifications()
        session.commit()
        flash('Message sent!', 'success')
    else:
        flash_errors(dmForm)

    return dmForm.redirect()


@users.route('/user/groups', methods=['GET', 'POST'])
@login_required
def myGroups():
    groupsImIn = current_user.accepted_groups
    groupsImInvitedTo = current_user.un_accepted_groups
    return render_template('group/myGroups.html',
                           acceptedGroups=groupsImIn,
                           invitedGroups=groupsImInvitedTo,
                           createGroupForm=CreateGroupForm(request.form),
                           title='My Groups')


@users.route('/user/updateProfilePicture', methods=['GET', 'POST'])
@login_required
def updateProfilePicture():
    picForm = ProfilePictureForm(request.form)
    if request.method == 'GET':
        return render_template('changeProfilePicture.html',
                               picForm=picForm)
    else:
        if 'profilePicture' not in request.files:
            flash('No file part', 'warning')
            return picForm.redirect()

        file = request.files['profilePicture']

        if file.filename == '':
            flash('No selected file', 'warning')
            return picForm.redirect()

        filename = secure_filename(request.files['profilePicture'].filename)

        if file and allowed_file(filename):
            # /uploads/users/1 .. ect
            userFilePath = "./nexnest/uploads/users/" + str(current_user.id)

            if not os.path.exists(userFilePath):
                os.makedirs(userFilePath)

            request.files['profilePicture'].save(userFilePath + '/' + filename)

            current_user.profile_image = '/uploads/users/' + \
                str(current_user.id) + '/' + filename

            session.commit()
            return redirect(url_for('users.viewUser', userID=current_user.id))
        else:
            flash("File doesn't exist or file extension is not allowed", 'danger')
            return picForm.redirect()


@users.route('/user/changePassword', methods=['GET', 'POST'])
@login_required
def changePassword():
    passForm = PasswordChangeForm(request.form)

    if passForm.validate():

        # Is the old password the same?
        if check_password(current_user, passForm.oldPassword.data):
            flash("Password Changed", 'success')
            current_user.set_password(passForm.newPassword.data)
            session.commit()
        else:
            flash("Password Change Failed, Old Password does not match", 'danger')
    else:
        flash_errors(passForm)

    return passForm.redirect()


@users.route('/user/getNotifications', methods=['GET', 'POST'])
@users.route('/user/getNotifications/<int:page>', methods=['GET', 'POST'])
@login_required
def getNotifications(page=1):
    app.logger.debug("/user/getNotifications page : %d" % page)

    allNotifications = Notification.query \
        .filter_by(target_user_id=current_user.id) \
        .filter(Notification.category.in_(('report_notification', 'generic_notification'))) \
        .distinct(Notification.notif_type,
                  Notification.redirect_url,
                  Notification.viewed) \
        .paginate(page, 10, False)

    app.logger.debug("allNotifications : %r" % allNotifications.items)

    allNotificationList = []
    for notif in allNotifications.items:
        allNotificationList.append(notif.serialize)

    numUnviewed = current_user.getUnreadNotificationCount()

    returnDict = {'numUnviewed': numUnviewed,
                  'notifications': allNotificationList}

    paginateDict = {
        'hasNext': allNotifications.has_next,
        'hasPrev': allNotifications.has_prev,
        'numPages': allNotifications.pages
    }

    returnDict['paginateDetails'] = paginateDict

    return jsonify(returnDict)


@users.route('/user/getMessageNotifications', methods=['GET', 'POST'])
@users.route('/user/getMessageNotifications/<int:page>', methods=['GET', 'POST'])
@login_required
def getMessageNotifications(page=1):
    from math import ceil
    app.logger.debug("/user/getMessageNotifications page : %d" % page)

    startNumber = None

    if page == 1:
        startNumber = 0
        endNumber = 10
    else:
        startNumber = (page * 10) - 10
        endNumber = (page * 10)

    directMessage = Notification.query.filter_by(
        user=current_user, category='direct_message')

    genericMessage = Notification.query.filter_by(
        user=current_user, category='generic_message')

    print('directMessage ', directMessage.all())
    print('generic ', genericMessage.all())

    print('Distinct')

    directMessage = directMessage.distinct(
        Notification.notif_type, Notification.viewed, Notification.target_model_id)
    genericMessage = genericMessage.distinct(
        Notification.notif_type, Notification.redirect_url, Notification.viewed)

    print('directMessage ', directMessage.all())
    print('generic ', genericMessage.all())

    compiledMessages = []
    allDirect = directMessage.all()
    allGeneric = genericMessage.all()

    compiledMessages.extend(allDirect)
    compiledMessages.extend(allGeneric)

    print('compiledMessages : \n %s' % pformat(compiledMessages))

    sortedCompiled = sorted(
        compiledMessages, key=lambda n: n.date_created, reverse=True)

    print('sortedCompiled : \n %s' % pformat(sortedCompiled))

    serializedReturn = []

    while startNumber < endNumber and startNumber < len(sortedCompiled):
        serializedReturn.append(sortedCompiled[startNumber].serialize)
        startNumber += 1

    numUnviewed = current_user.getUnreadMessageNotificationCount()

    returnDict = {'numUnviewed': numUnviewed,
                  'notifications': serializedReturn}

    paginateDict = {
        'hasNext': (endNumber < len(compiledMessages)),
        'hasPrev': (endNumber - 10) > 0,
        'numPages': int((len(compiledMessages) / 10)) + 1
    }

    returnDict['paginateDetails'] = paginateDict

    return jsonify(returnDict)


@users.route('/user/favoriteListing/<listingID>', methods=['GET', 'POST'])
@login_required
@csrf.exempt
def favoriteListing(listingID):
    listing = session.query(Listing).filter_by(id=listingID).first_or_404()

    # Make sure one doesn't already exist
    lf = ListingFavorite.query.filter_by(
        listing=listing, user=current_user).first()

    if lf is None:
        app.logger.debug("Listing %r" % listing)
        newFavorite = ListingFavorite(user=current_user,
                                      listing=listing)

        app.logger.debug("ListingFavorite %r" % newFavorite)
        session.add(newFavorite)
        session.commit()
    else:
        return jsonify(response={'success': False, 'message': 'Listing has already been favorited'})

    return jsonify(response={'success': True})


@users.route('/user/unFavoriteListing/<listingID>', methods=['GET', 'POST'])
@login_required
@csrf.exempt
def unFavoriteListing(listingID):
    listing = session.query(Listing).filter_by(id=listingID).first_or_404()

    app.logger.debug("Listing %r" % listing)
    listingFavorite = session.query(ListingFavorite).filter_by(
        listing=listing, user=current_user).first()

    app.logger.debug("ListingFavorite %r" % listingFavorite)
    session.delete(listingFavorite)
    session.commit()
    return jsonify("true")


@users.route('/landlord/getAvailability/JSON', methods=['GET'])
@users.route('/landlord/getAvailability/JSON/<landlordID>', methods=['GET'])
@login_required
def getAvailability(landlordID=None):
    if landlordID is None:
        landlordID = current_user.id

    availabilityList = []

    for i in range(7):
        availabilities = Availability.query \
            .filter_by(landlord_id=landlordID, day=i) \
            .order_by(Availability.time.asc()) \
            .all()

        for avail in availabilities:
            availabilityList.append(avail.serialize)

    return jsonify(availabilityList)


@users.route('/user/passwordReset/<email>')
def resetPassword(email):
    user = User.query.filter_by(email=email).first_or_404()

    emailConfirmURL = url_for('users.resetPasswordConfirm',
                              payload=generate_confirmation_token(user.email),
                              _external=True)

    # Send EMAIL
    user.sendEmail('passwordReset', genEmailPasswordResetContent(user, emailConfirmURL))

    flash('Password Reset Email sent to %s' % email, 'success')
    return redirect(url_for('users.login'))


@users.route('/user/password/reset/<payload>', methods=['GET', 'POST'])
def resetPasswordConfirm(payload):
    try:
        email = confirm_token(payload)
    except:
        flash('The confirmation link is invalid or has expired.', 'danger')
        app.logger.warning('User just tried to reset password with an invalid or expired token')
        abort(404)

    user = User.query.filter_by(email=email).first_or_404()
    form = NewPasswordForm()

    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()

        flash('Password updated!', 'success')
        return redirect(url_for('indexs.index'))
    else:
        flash_errors(form)

    return render_template('resetPassword.html', form=form, payload=payload)


@users.route('/user/forgotPassword', methods=['GET', 'POST'])
def forgotPassword():
    return render_template('forgotPassword.html', title="Forgot Password")
