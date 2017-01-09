from flask import Blueprint
from flask import render_template, request, redirect, url_for

from flask_login import login_user

from nexnest.application import session

from nexnest.models.user import User

from nexnest.forms.register_form import RegistrationForm

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
