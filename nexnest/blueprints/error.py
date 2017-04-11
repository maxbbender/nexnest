from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required

from nexnest.forms import LoginForm
from nexnest.application import session
from nexnest import app

errors = Blueprint('errors', __name__, template_folder='../templates/errors')

@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template('500.html'), 500