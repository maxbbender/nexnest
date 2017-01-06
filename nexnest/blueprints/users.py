from flask import Blueprint
from flask import render_template, request

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
                       registerForm.name.data)

        session.add(newUser)
        session.commit()
        return 'ye'
    else:
        return render_template('register.html', registration_form=registerForm)
