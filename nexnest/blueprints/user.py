from flask import Blueprint
from flask import render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_user, logout_user, current_user

from nexnest.application import session

from nexnest.models.user import User
from nexnest.models.group import Group

from nexnest.forms.register_form import RegistrationForm
from nexnest.forms.loginForm import LoginForm
from nexnest.forms.editAccountForm import EditAccountForm

from nexnest.utils.password import check_password
from nexnest.utils.flash import flash_errors

from sqlalchemy import func

users = Blueprint('users', __name__, template_folder='../templates/user')


@users.route('/register', methods=['GET'])
def register():
    return render_template('register.html',
                           registration_form=RegistrationForm())


@users.route('/process_registration', methods=['POST'])
def create():
    registerForm = RegistrationForm(request.form)

    if registerForm.validate():
        newUser = User(registerForm.email.data,
                       registerForm.password.data,
                       registerForm.fname.data,
                       registerForm.lname.data)

        session.add(newUser)
        session.commit()

        login_user(newUser)

        return redirect(url_for('indexs.index'))
    else:
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
    #form.school.data = current_user.school
    if form.validate_on_submit():
        current_user.fname = form.fname.data
        current_user.lname = form.lname.data
        current_user.email = form.email.data
        current_user.website = form.website.data
        current_user.bio = form.bio.data
        current_user.phone = form.phone.data
        #current_user.school = form.school.data
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


@users.route('/search/<username>')
def searchForUser(username):
    usersToReturn = session.query(User).filter(func.lower(
        User.username).like(func.lower(username + "%"))).all()

    return jsonify(usersToReturn)

@users.route('/acceptGroupInvite/<groupID>')
def acceptGroupInvite(groupID):
    group = session.query(Group).filter_by(id=groupID).first()
    current_user.accept_group_invite(group)
    return redirect(url_for('groups.viewGroup', group_id=group.id))

@users.route('/declineGroupInvite/<groupID>')
def declineGroupInvite(groupID):
    group = session.query(Group).filter_by(id=groupID).first()
    current_user.decline_group_invite(group)
    return redirect(url_for('groups.myGroups'))

