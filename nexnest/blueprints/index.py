from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from flask import current_app as app

from nexnest import db
from nexnest.forms import LoginForm
from nexnest.models.listing import Listing
from nexnest.models.user import User
from nexnest.utils.email import send_email
from nexnest.utils.school import allSchoolsAsStrings, allSchools
from nexnest.static.dataSets import valid_time_frames

session = db.session

indexs = Blueprint('indexs', __name__, template_folder='../templates')


@indexs.route('/')
@indexs.route('/index')
@indexs.route('/index#search')
def index():
    form = LoginForm(request.form)
    allListings = session.query(Listing).all()
    featuredListings = session.query(Listing).all()

    if request.method == 'POST' and form.validate():
        # user = User(form.username.data, form.email.data,
        #            form.password.data)
        # db_session.add(user)
        flash('Login Successfull')
        return redirect(url_for('indexs.index'))

    return render_template('index.html',
                           form=form,
                           listings=allListings,
                           featuredListings=featuredListings,
                           title='NexNest',
                           schools=allSchoolsAsStrings(),
                           validTimeFrames=valid_time_frames)


@indexs.route('/test')
@login_required
def test():
    app.logger.warning('yooo')
    return render_template('test.html')


@indexs.route('/faq')
def faq():
    return render_template('faq.html',
                           title='FAQ')


@indexs.route('/aboutUs')
def aboutUs():
    return render_template('aboutUs.html',
                           title='About Us')


@indexs.route('/privacyPolicy')
def privacyPolicy():
    return render_template('privacyPolicy.html',
                           title='Privacy Policy')


@indexs.route('/termsConditions')
def termsConditions():
    return render_template('termsConditions.html',
                           title='Terms and Conditions')


# TEST FOR EMAILS
@indexs.route('/groupMessageEmail')
def groupMessageEmail():
    return render_template('email/newGroupMessageEmail.html',
                           title='Email')
