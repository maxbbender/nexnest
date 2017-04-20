# Application Config

# Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, current_user
from flask_wtf.csrf import CSRFProtect

# Session|Engine(SQLAlchemy)
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy import create_engine

from nexnest import app

# DB setup
# engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
# session = scoped_session(sessionmaker(bind=engine))
db = SQLAlchemy(app)
session = db.session

# CSRF setup
csrf = CSRFProtect(app)

# Login Manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = '/login'

import braintree


braintree.Configuration.configure(braintree.Environment.Sandbox,
                                  merchant_id="95d9g95dztdsgkkh",
                                  public_key="fdtk8w9qbpvqr6kn",
                                  private_key="ec367f7335d5e9c222656212e1ff78f2")

# Our Models
# from nexnest.models import *
# from nexnest.models import base
# # from nexnest.models import direct_message
# from nexnest.models import notification
# from nexnest.models import user

# from nexnest.models import direct_message
# from nexnest.models.direct_message import DirectMessage


@login_manager.user_loader
def load_user(user_id):
    from nexnest.models.user import User
    return session.query(User).filter_by(id=user_id).first()

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

from nexnest.forms import LoginForm, PasswordChangeForm, ProfilePictureForm


@app.context_processor
def insert_login_form():
    if current_user.is_authenticated:
        passwordChangeForm = PasswordChangeForm()
        avatarChangeForm = ProfilePictureForm()
        # messages, notifications = current_user.unreadNotifications()
        notifications = current_user.getNotifications()

        numUnviewed = 0
        for notif in notifications:
            if not notif.viewed:
                numUnviewed += 1

        messages = current_user.getMessageNotifications()

        numUnviewedMessages = 0
        for notif in messages:
            if not notif.viewed:
                numUnviewedMessages += 1

        return dict(passwordChangeForm=passwordChangeForm,
                    avatarChangeForm=avatarChangeForm,
                    notifications=notifications,
                    numUnviewedNotifications=numUnviewed,
                    numUnviewedMessages=numUnviewedMessages,
                    notificationMessages=messages)
    else:
        login_form = LoginForm()
        return dict(login_form=login_form)

import nexnest.admin  # pylint: disable=unused-import
