from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required

from nexnest import app
from nexnest.forms import LoginForm
from nexnest.application import session
from nexnest.models.listing import Listing
from nexnest.models.user import User
from nexnest.utils.email import send_email


indexs = Blueprint('indexs', __name__, template_folder='../templates')


@indexs.route('/')
@indexs.route('/index')
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
                           title='NexNest')


@indexs.route('/test')
@login_required
def test():
    # send_email('Dom', 'no_reply@nexnest.com', ['maxbbender@gmail.com'], 'Hey You', None)
    # user = User.query.first()
    # emailSend = user.sendEmail(emailType='message', message='domislove')
    # print(emailSend)
    # return render_template('test.html')
    return str(app.config['TESTING'])
