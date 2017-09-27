# Nexnest Application Startpoint

# OS Functions
import os
from os import environ
from os.path import dirname, exists, join

import braintree
from config import config
# Flask
from flask import Flask, redirect, render_template, url_for
from flask_admin import Admin
from flask_login import LoginManager, current_user
from flask_mail import Mail, email_dispatched
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect

db = SQLAlchemy()
mail = Mail()
csrf = CSRFProtect()
login_manager = LoginManager()
admin = Admin(name='Nexnest', template_mode='bootstrap3')


def createApp(configName):
    app = Flask(__name__)
    app.config.from_object(config[configName])
    config[configName].init_app(app)

    db.init_app(app)
    mail.init_app(app)
    csrf.init_app(app)
    login_manager.init_app(app)
    admin.init_app(app)

    login_manager.login_view = '/login'

    @login_manager.user_loader
    def load_user(user_id):
        from nexnest.models.user import User
        return db.session.query(User).filter_by(id=user_id).first()

    if app.config['BRAINTREE_ENV'] == 'sandbox':
        braintree.Configuration.configure(braintree.Environment.Sandbox,
                                          merchant_id=app.config['BRAINTREE_MERCHANT_ID'],
                                          public_key=app.config['BRAINTREE_PUBLIC_KEY'],
                                          private_key=app.config['BRAINTREE_PRIVATE_KEY'])
    elif app.config['BRAINTREE_ENV'] == 'production':
        braintree.Configuration.configure(braintree.Environment.Production,
                                          merchant_id=app.config['BRAINTREE_MERCHANT_ID'],
                                          public_key=app.config['BRAINTREE_PUBLIC_KEY'],
                                          private_key=app.config['BRAINTREE_PRIVATE_KEY'])
    else:
        app.logger.error('Unknown BRAINTREE_ENV : %s' % app.config['BRAINTREE_ENV'])

    # Blueprints
    from nexnest.blueprints.base import base
    from nexnest.blueprints.index import indexs
    from nexnest.blueprints.listing import listings
    from nexnest.blueprints.user import users
    from nexnest.blueprints.group import groups
    from nexnest.blueprints.tour import tours
    from nexnest.blueprints.landlord import landlords
    from nexnest.blueprints.housingRequest import housingRequests
    from nexnest.blueprints.house import houses
    from nexnest.blueprints.commerce import commerce
    from nexnest.blueprints.error import errors
    from nexnest.blueprints.notification import notifications
    from nexnest.blueprints.report import reports
    from nexnest.blueprints.rent import rents
    from nexnest.blueprints.siteAdmin import siteAdmin as siteAdminBlueprint

    app.register_blueprint(base)
    app.register_blueprint(indexs)
    app.register_blueprint(listings)
    app.register_blueprint(users)
    app.register_blueprint(groups)
    app.register_blueprint(tours)
    app.register_blueprint(landlords)
    app.register_blueprint(housingRequests)
    app.register_blueprint(houses)
    app.register_blueprint(commerce)
    app.register_blueprint(errors)
    app.register_blueprint(notifications)
    app.register_blueprint(reports)
    app.register_blueprint(rents)
    app.register_blueprint(siteAdminBlueprint, url_prefix='/siteAdmin')

    @login_manager.unauthorized_handler
    def unauthorized():
        app.logger.warning('User unauthorized')
        # do stuff
        return redirect(url_for('users.login'))

    from nexnest.forms import LoginForm, PasswordChangeForm, ProfilePictureForm, PlatformReportForm, DirectMessageForm, ContactForm

    @app.context_processor
    def insert_login_form():
        if current_user.is_authenticated:
            passwordChangeForm = PasswordChangeForm()
            avatarChangeForm = ProfilePictureForm()
            dmForm = DirectMessageForm()
            # messages, notifications = current_user.unreadNotifications()
            notifications = current_user.getNotifications()
            messages = current_user.getMessageNotifications()
            houses = current_user.houseList

            numUnviewedNotifications = current_user.getUnreadNotificationCount()
            numUnviewedMessages = current_user.getUnreadMessageNotificationCount()

            return dict(passwordChangeForm=passwordChangeForm,
                        avatarChangeForm=avatarChangeForm,
                        notifications=notifications,
                        numUnviewedNotifications=numUnviewedNotifications,
                        numUnviewedMessages=numUnviewedMessages,
                        notificationMessages=messages,
                        platformReportForm=PlatformReportForm(),
                        DirectMessageForm=DirectMessageForm(),
                        houses=houses,
                        dmForm=dmForm,
                        contactForm=ContactForm())
        else:
            login_form = LoginForm()
            dmForm = DirectMessageForm()

            return dict(login_form=login_form,
                        platformReportForm=PlatformReportForm(),
                        dmForm=dmForm,
                        contactForm=ContactForm())

    import nexnest.admin

    def format_datetime(value, format='human'):
        if format == 'human':
            format = '%B %m, %Y at %-I:%-M%p'
        return value.strftime(format)

    def format_date(value, format='human'):
        if format == 'human':
            format = '%B %m, %Y'
        return value.strftime(format)

    app.jinja_env.filters['format_datetime'] = format_datetime
    app.jinja_env.filters['format_date'] = format_date

    @app.context_processor
    def override_url_for():
        return dict(url_for=dated_url_for)

    def dated_url_for(endpoint, **values):
        if endpoint == 'static':
            filename = values.get('filename', None)
            if filename:
                file_path = os.path.join(app.root_path,
                                         endpoint, filename)
                values['q'] = int(os.stat(file_path).st_mtime)
        return url_for(endpoint, **values)

    # CSRF Error Handler
    from flask_wtf.csrf import CSRFError
    from flask import abort, flash

    @app.errorhandler(CSRFError)
    def handle_csrf_error(e):
        app.logger.warning('CSRF error : %r' % e)
        flash('CSRF Error. Please refresh the page and try again.', 'warning')
        return abort(405)

    return app


def logEmailDispatch(message, app):
    app.logger.debug('Email Sent! Subject %s | Text %s' % (message.subject, message.html))


email_dispatched.connect(logEmailDispatch)
