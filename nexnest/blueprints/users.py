from flask import Blueprint
from flask import render_template, request, redirect, url_for, flash

from flask_login import login_user, logout_user

from nexnest.application import session

from nexnest.models.user import User

from nexnest.forms.register_form import RegistrationForm
from nexnest.forms.loginForm import LoginForm

from nexnest.utils.password import check_password
from nexnest.utils.flash import flash_errors

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


@users.route('/logout')
def logout():
    logout_user()
    return redirect("/")
