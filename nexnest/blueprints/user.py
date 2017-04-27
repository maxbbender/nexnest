from flask import Blueprint
from flask import render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_user, logout_user, current_user, login_required

from nexnest import logger
from nexnest.application import session

from nexnest.models.user import User
from nexnest.models.group import Group
from nexnest.models.school import School
from nexnest.models.direct_message import DirectMessage
from nexnest.models.notification import Notification
from nexnest.models.notification_preference import NotificationPreference
from nexnest.models.listing_favorite import ListingFavorite
from nexnest.models.listing import Listing

from nexnest.forms import RegistrationForm, LoginForm, EditAccountForm, DirectMessageForm, ProfilePictureForm, PasswordChangeForm, CreateGroupForm, EmailPreferencesForm

from nexnest.utils.password import check_password
from nexnest.utils.flash import flash_errors
from nexnest.utils.file import allowed_file
from nexnest.utils.email import generate_confirmation_token, confirm_token

from sqlalchemy import func, asc, or_, and_

from werkzeug.utils import secure_filename

import os

from itsdangerous import BadSignature

users = Blueprint('users', __name__, template_folder='../templates/user')


@users.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        schools = [r for r, in session.query(School.name).all()]
        return render_template('register.html',
                               registration_form=RegistrationForm(),
                               schools=schools)
    else:  # Post
        registerForm = RegistrationForm(request.form)

        if registerForm.validate():
            # First make sure that the school is valid
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
            else:
                flash("School you selected doesn't exist", 'warning')

        return render_template('register.html', registration_form=registerForm)


@users.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        # print(request.args['next'])
        # print(request.args.get['next'])
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

        if login_form.next.data == '':
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

    form = EmailPreferencesForm(request.form)
    user = session.query(User).filter_by(id=userID).first()
    currentPreferences = session.query(
            NotificationPreference).filter_by(user_id=userID).first()
    logger.debug(currentPreferences)
    form = EmailPreferencesForm(obj=currentPreferences)

    if request.method == 'GET':
        return render_template('/user/account.html',
                               user=user, 
                               form=form,
                               title=user.fname
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
            currentPreferences.group_listing_completed_email = form.group_listing_completed_email.data
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


@users.route('/user/edit/info', methods=['GET', 'POST'])
@login_required
def editAccountInfo():
    editForm = EditAccountForm(request.data, obj=current_user)
    editForm.school.data = current_user.school.name

    if request.method == 'POST' and editForm.validate():
        editForm.populate_obj(current_user)
        session.commit()
        return redirect(url_for('users.viewUser', userID=current_user.id))

    schools = [r for r, in session.query(School.name).all()]
    return render_template('editAccount.html',
                           form=editForm,
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
    return redirect(url_for('groups.viewGroup', group_id=group.id))


@users.route('/user/declineGroupInvite/<groupID>')
@login_required
def declineGroupInvite(groupID):
    group = session.query(Group).filter_by(id=groupID).first()
    current_user.decline_group_invite(group)
    return redirect(url_for('groups.myGroups'))


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
def favoriteListing(listingID):
    listing = session.query(Listing).filter_by(id=listingID).first()

    logger.debug("Listing %r" % listing)
    newFavorite = ListingFavorite(user=current_user,
                                  listing=listing)

    logger.debug("ListingFavorite %r" % newFavorite)
    session.add(newFavorite)
    session.commit()
    return jsonify("true")

@users.route('/user/unFavoriteListing/<listingID>', methods=['GET', 'POST'])
@login_required
def unFavoriteListing(listingID):
    listing = session.query(Listing).filter_by(id=listingID).first()

    logger.debug("Listing %r" % listing)
    listingFavorite = session.query(ListingFavorite).filter_by(listing=listing, user=current_user).first()

    logger.debug("ListingFavorite %r" % listingFavorite)
    session.delete(listingFavorite)
    session.commit()
    return jsonify("true")
