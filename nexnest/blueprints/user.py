from flask import Blueprint
from flask import render_template, request, redirect, url_for, flash, jsonify, abort
from flask_login import login_user, logout_user, current_user, login_required

from nexnest import logger
from nexnest.application import session, csrf, app

from nexnest.models.user import User
from nexnest.models.group import Group
from nexnest.models.group_email import GroupEmail
from nexnest.models.group_user import GroupUser
from nexnest.models.school import School
from nexnest.models.direct_message import DirectMessage
from nexnest.models.notification import Notification
from nexnest.models.notification_preference import NotificationPreference
from nexnest.models.listing_favorite import ListingFavorite
from nexnest.models.listing import Listing
from nexnest.models.landlord import Landlord
from nexnest.models.availability import Availability

from nexnest.forms import RegistrationForm, LoginForm, EditAccountForm, DirectMessageForm, ProfilePictureForm, PasswordChangeForm, CreateGroupForm, EmailPreferencesForm, LandlordMoreInfoForm, LandlordEditAccountForm
from nexnest.utils.school import allSchoolsAsStrings
from nexnest.utils.password import check_password
from nexnest.utils.flash import flash_errors
from nexnest.utils.file import allowed_file
from nexnest.utils.email import generate_confirmation_token, confirm_token

from nexnest.decorators import user_editable

from sqlalchemy import func, asc, or_, and_

from werkzeug.utils import secure_filename

import os

from itsdangerous import BadSignature

users = Blueprint('users', __name__, template_folder='../templates/user')


@users.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        if current_user.is_authenticated:
            return redirect(url_for('indexs.index'))

        #schools = [r for r, in session.query(School.name).all()]
        return render_template('register.html',
                               form=RegistrationForm(),
                               schools=allSchoolsAsStrings())
    else:  # Post
        registerForm = RegistrationForm(request.form)

        if registerForm.validate():
            # Determine if registering as tenant or landlord
            userType = registerForm.landlord.data

            if userType == "landlord":
                newUser = User(email=registerForm.email.data,
                               password=registerForm.password.data,
                               fname=registerForm.fname.data,
                               lname=registerForm.lname.data)
                session.add(newUser)
                session.commit()

                # Make them a Landlord

                # Notification Preference Table init
                session.add(NotificationPreference(user=newUser))
                session.commit()

                return redirect(url_for('users.landlordInformation', userID=newUser.id))

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
                    session.add(NotificationPreference(user=newUser))
                    session.commit()

                    emailConfirmURL = url_for('users.emailConfirm', payload=generate_confirmation_token(newUser.email), _external=True)
                    newUser.sendEmail('generic',
                                      'Click the link to confirm your account <a href="%s">Click Here</a>' % emailConfirmURL)

                    return redirect(url_for('users.emailConfirmNotice', email=registerForm.email.data))
        flash_errors(registerForm)
        return render_template('register.html', form=registerForm, schools=allSchoolsAsStrings())


# BRAINTREE UPDATE
@users.route('/register/<userID>/landlordInformation', methods=['GET', 'POST'])
def landlordInformation(userID):
    if request.method == 'GET':

        return render_template('landlordMoreInformation.html',
                               form=LandlordMoreInfoForm(),
                               userID=userID)
    else:  # Post
        moreInformationForm = LandlordMoreInfoForm(request.form)

        if moreInformationForm.validate():
            user = session.query(User).filter_by(id=userID).first()
            newLandlord = Landlord(user=user,
                                   street=moreInformationForm.street.data,
                                   city=moreInformationForm.city.data,
                                   state=moreInformationForm.state.data,
                                   zip_code=moreInformationForm.zip_code.data,
                                   check_pay=moreInformationForm.check_pay.data,
                                   online_pay=moreInformationForm.online_pay.data)

            session.add(newLandlord)
            session.commit()

            newLandlord.user.dob = moreInformationForm.date_of_birth.data
            newLandlord.user.phone = moreInformationForm.phone.data
            session.commit()

            flash('Theoretically this all worked', 'info')
            emailConfirmURL = url_for('users.emailConfirm', payload=generate_confirmation_token(user.email), _external=True)
            user.sendEmail('generic',
                           'Click the link to confirm your account <a href="%s">Click Here</a>' % emailConfirmURL)

            return redirect(url_for('users.emailConfirmNotice', email=user.email))
            # MAX DO YOUR MAGIC HERE
        flash_errors(moreInformationForm)
        return render_template('/landlordMoreInformation.html', form=moreInformationForm, userID=userID)


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
                            groupEmailInvites = GroupEmail.query.filter_by(email=user.email, used=False).all()

                            if len(groupEmailInvites) > 0:
                                for groupEmail in groupEmailInvites:
                                    groupUserCheck = GroupUser.query.filter_by(group=groupEmail.group, user=user).count()
                                    errorMessage = None
                                    if groupUserCheck == 0:
                                        newGroupUser = GroupUser(groupEmail.group, user)
                                        newGroupUser.accepted = True
                                        groupEmail.used = True
                                        session.add(newGroupUser)
                                        session.commit()
                                    else:
                                        groupEmail.used = True
                                        session.commit()

                        else:
                            flash('You must confirm your email before logging in', 'danger')
                    else:
                        flash("Error validating login credentials", 'danger')
                else:
                    flash("User account has been deleted", 'warning')
            else:
                flash("User not found", 'warning')
        else:
            flash_errors(login_form)

        if user.isLandlord:
            return redirect('/landlord/dashboard')

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
        flash('You have confirmed your account. Thanks!', 'success')

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
        userFavorites = session.query(ListingFavorite).filter_by(user=current_user).all()
        myGroups = current_user.accepted_groups
        logger.debug(currentPreferences)
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
        logger.warning('User %r attempted to access user_ids page %s' % (current_user, userID))
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

        if form.dob.data != '':
            current_user.dob = form.dob.data

        current_user.bio = form.bio.data
        current_user.phone = form.phone.data
        current_user.email = form.email.data

        if currentUserIsLandlord:
            landlord.online_pay = form.online_pay.data
            landlord.check_pay = form.check_pay.data
            landlord.street = form.street.data
            landlord.city = form.city.data
            landlord.zip_code = form.zip_code.data
            landlord.state = form.state.data
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
        form.dob.data = current_user.dob
        form.bio.data = current_user.bio
        form.phone.data = current_user.phone
        form.email.data = current_user.email

        return render_template( 'editAccount.html',
                               form=form,
                               title='Edit Account',
                               schools=None)
    else:
        schools = [r for r, in session.query(School.name).all()]
        form = EditAccountForm(request.form, obj=current_user)
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
    userList = []
    direct_messages = session.query(DirectMessage.target_user_id) \
        .filter_by(source_user_id=current_user.id) \
        .order_by('date_created desc') \
        .group_by(DirectMessage.target_user_id) \
        .limit(1)

    for dm in direct_messages:
        user = session.query(User).filter_by(id=dm).first()
        userList.append(user)

    return render_template('directMessageAll.html',
                           users=userList)


@users.route('/user/directMessages/<user_id>')
@login_required
def directMessagesIndividual(user_id):
    target_user = session.query(User) \
        .filter_by(id=user_id) \
        .first()

    dm = session.query(DirectMessage) \
        .filter(or_(
            (and_(DirectMessage.source_user_id == current_user.id,
                  DirectMessage.target_user_id == user_id)),
            (and_(DirectMessage.target_user_id == current_user.id,
                  DirectMessage.source_user_id == user_id)))) \
        .order_by(asc(DirectMessage.date_created)) \
        .all()

    msgForm = DirectMessageForm(target_user_id=user_id)

    return render_template('directMessageIndividual.html',
                           target_user=target_user,
                           dm=dm,
                           msgForm=msgForm)


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
    else:
        flash_errors(dmForm)

    return redirect(url_for('users.directMessagesIndividual',
                            user_id=dmForm.target_user_id.data))


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
    logger.debug("/user/getNotifications page : %d" % page)

    allNotifications = Notification.query \
        .filter_by(target_user_id=current_user.id) \
        .filter(Notification.category.in_(('report_notification', 'generic_notification'))) \
        .distinct(Notification.notif_type,
                  Notification.redirect_url,
                  Notification.viewed) \
        .paginate(page, 10, False)

    logger.debug("allNotifications : %r" % allNotifications.items)

    allNotificationList = []
    for notif in allNotifications.items:
        allNotificationList.append(notif.serialize)

    numUnviewed = current_user.getUnreadNotificationCount()

    returnDict = {'numUnviewed': numUnviewed, 'notifications': allNotificationList}

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
    logger.debug("/user/getMessageNotifications page : %d" % page)

    allNotifications = Notification.query \
        .filter_by(target_user_id=current_user.id) \
        .filter(Notification.category.in_(('direct_message', 'generic_message'))) \
        .distinct(Notification.notif_type,
                  Notification.redirect_url,
                  Notification.viewed) \
        .paginate(page, 10, False)

    logger.debug("allNotifications : %r" % allNotifications.items)

    allNotificationList = []

    for notif in allNotifications.items:
        allNotificationList.append(notif.serialize)

    numUnviewed = current_user.getUnreadMessageNotificationCount()

    returnDict = {'numUnviewed': numUnviewed, 'notifications': allNotificationList}

    paginateDict = {
        'hasNext': allNotifications.has_next,
        'hasPrev': allNotifications.has_prev,
        'numPages': allNotifications.pages
    }

    returnDict['paginateDetails'] = paginateDict

    return jsonify(returnDict)


@users.route('/user/favoriteListing/<listingID>', methods=['GET', 'POST'])
@login_required
@csrf.exempt
def favoriteListing(listingID):
    listing = session.query(Listing).filter_by(id=listingID).first_or_404()

    # Make sure one doesn't already exist
    lf = ListingFavorite.query.filter_by(listing=listing, user=current_user).first()

    if lf is None:
        logger.debug("Listing %r" % listing)
        newFavorite = ListingFavorite(user=current_user,
                                      listing=listing)

        logger.debug("ListingFavorite %r" % newFavorite)
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

    logger.debug("Listing %r" % listing)
    listingFavorite = session.query(ListingFavorite).filter_by(listing=listing, user=current_user).first()

    logger.debug("ListingFavorite %r" % listingFavorite)
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
