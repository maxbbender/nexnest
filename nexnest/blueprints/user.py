from flask import Blueprint
from flask import render_template, abort, request, redirect, url_for, flash, jsonify

from nexnest.forms.register_form import ExtendedRegistrationForm

users = Blueprint('users', __name__, template_folder='../templates')


@users.route('/register')
def register():
    register_form = ExtendedRegistrationForm()
    return render_template('security/register_user.html',
                           register_user_form=register_form)
