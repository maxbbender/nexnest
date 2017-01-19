from flask import Blueprint
from flask import render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_user, logout_user, current_user, login_required

from nexnest.application import session

from nexnest.models.user import User
from nexnest.models.group import Group
from nexnest.models.school import School
from nexnest.models.direct_message import DirectMessage

from nexnest.forms.register_form import RegistrationForm
from nexnest.forms.loginForm import LoginForm
from nexnest.forms.editAccountForm import EditAccountForm
from nexnest.forms.directMessageForm import DirectMessageForm

from nexnest.utils.password import check_password
from nexnest.utils.flash import flash_errors

from sqlalchemy import func, asc, or_, and_

users = Blueprint('users', __name__, template_folder='../templates/user')


@users.route('/register', methods=['GET'])
def register():
    schools = [r for r, in session.query(School.name).all()]
    return render_template('register.html',
                           registration_form=RegistrationForm(),
                           schools=schools)


@users.route('/process_registration', methods=['POST'])
def create():
    registerForm = RegistrationForm(request.form)

    if registerForm.validate():
        # First make sure that the school is valid
        school = session.query(School).filter(func.lower(
            School.name) == registerForm.school.data.lower()).first()

        if school is not None:
            # School Exists
            newUser = User(email=registerForm.email.data,
                           password=registerForm.password.data,
                           fname=registerForm.fname.data,
                           lname=registerForm.lname.data,
                           school=school)

            session.add(newUser)
            session.commit()

            login_user(newUser)

            return redirect(url_for('indexs.index'))
        else:
            flash("School you selected doesn't exist", 'warning')

    return render_template('register.html', registration_form=registerForm)


@users.route('/login', methods=['GET'])
def login():
    return render_template('login.html', login_form=LoginForm())


@users.route('/login', methods=['POST'])
def process_login():
    login_form = LoginForm(request.form)

    if login_form.validate():

        user = session.query(User).filter_by(
            email=login_form.email.data).first()

        # Does the user exist
        if user is not None:
            if user.active is True:

                if check_password(user, login_form.password.data):
                    login_user(user)
                    return redirect('/')
                else:
                    flash("Error validating login credentials")
            else:
                flash("User account has been deleted")
        else:
            flash("User not found")
    else:
        flash_errors(login_form)

    return redirect(url_for('users.login'))


@users.route('/viewUser/<userID>', methods=['GET', 'POST'])
def viewUser(userID):
    # fake lisiting for testing
    user = session.query(User).filter_by(id=userID).first()
    return render_template('userAccount.html', user=user, title=user.fname)


@users.route('/editAccount', methods=['GET', 'POST'])
def editAccount():
    currentUser = session.query(User).filter_by(id=current_user.id).first()
    form = EditAccountForm(obj=currentUser)
    # if request.method == 'GET':
    #     form.fname.data = current_user.fname
    #     form.lname.data = current_user.lname
    #     form.email.data = current_user.email
    #     form.website.data = current_user.website
    #     form.bio.data = current_user.bio
    #     form.phone.data = current_user.phone
    # form.school.data = current_user.school
    if form.validate_on_submit():
        current_user.fname = form.fname.data
        current_user.lname = form.lname.data
        current_user.email = form.email.data
        current_user.website = form.website.data
        current_user.bio = form.bio.data
        current_user.phone = form.phone.data
        # current_user.school = form.school.data
        if not form.password.data == '':
            current_user.set_password(form.password.data)
        session.commit()
        flash('Account Updated', 'info')
        return redirect(url_for('viewUsers.viewUser', userID=current_user.id))
    return render_template('/editAccount.html', form=form, title='Edit Account')


@users.route('/logout')
def logout():
    logout_user()
    return redirect("/")


@users.route('/user/search/<username>')
def searchForUser(username):
    usersToReturn = session.query(User).filter(func.lower(
        User.username).like(func.lower(username + "%"))).all()

    return jsonify(users=[i.serialize for i in usersToReturn])


@users.route('/user/acceptGroupInvite/<groupID>')
def acceptGroupInvite(groupID):
    group = session.query(Group).filter_by(id=groupID).first()
    current_user.accept_group_invite(group)
    return redirect(url_for('groups.viewGroup', group_id=group.id))


@users.route('/user/declineGroupInvite/<groupID>')
def declineGroupInvite(groupID):
    group = session.query(Group).filter_by(id=groupID).first()
    current_user.decline_group_invite(group)
    return redirect(url_for('groups.myGroups'))


@users.route('/user/search/<username>/<group_id>')
def searchForGroupUser(username, group_id):
    usersToReturn = session.query(User).filter(func.lower(
        User.username).like(func.lower(username + "%"))).all()

    group = session.query(Group).filter_by(id=group_id).first()

    users = []
    apartOfGroup = False
    for user in usersToReturn:
        if user.isLandlord:
            continue

        for groupUser in user.groups:
            if groupUser.group == group:
                apartOfGroup = True
                break
        if not apartOfGroup:
            users.append(user.serialize)
        else:
            apartOfGroup = False

    return jsonify(users=users)


@users.route('/user/directMessages')
@login_required
def directMessagesAll():
    users = []
    direct_messages = session.query(DirectMessage.target_user_id) \
        .filter_by(source_user_id=current_user.id) \
        .group_by(DirectMessage.target_user_id) \
        .all()

    for dm in direct_messages:
        user = session.query(User).filter_by(id=dm).first()
        users.append(user)

    return render_template('directMessageAll.html',
                           users=users)


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
                           title='My Groups')
