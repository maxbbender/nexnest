# Nexnest Application Startpoint

# OS Functions
from os import environ
from os.path import join
from os.path import dirname

from dotenv import load_dotenv

# Flask
from flask import Flask, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, current_user
from flask_wtf.csrf import CSRFProtect

# Session|Engine(SQLAlchemy)
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy import create_engine

# DotEnv Setup
load_dotenv(join(dirname(__file__), '..', '.env'))

# Environment choice
env = environ.get('NEXNEST_ENV')

if env is None:
    env = 'development'

# File Uploads
UPLOAD_FOLDER = dirname(__file__) + '/uploads'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

# App setup
app = Flask(__name__, static_folder="static")
app.config.from_envvar('NEXNEST_%s_SETTINGS' % env.upper())
app.secret_key = 'domislove'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


# DB setup
engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
session = scoped_session(sessionmaker(bind=engine))
db = SQLAlchemy(app)

# CSRF setup
csrf = CSRFProtect(app)

# Login Manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = '/login'

# Our Models
from nexnest.models import *


@login_manager.user_loader
def load_user(user_id):
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

app.register_blueprint(base)
app.register_blueprint(indexs)
app.register_blueprint(listings)
app.register_blueprint(users)
app.register_blueprint(groups)
app.register_blueprint(tours)
app.register_blueprint(landlords)
app.register_blueprint(housingRequests)
app.register_blueprint(houses)

from nexnest.forms import LoginForm, PasswordChangeForm, ProfilePictureForm


@app.context_processor
def insert_login_form():
    if current_user.is_authenticated:
        passwordChangeForm = PasswordChangeForm()
        avatarChangeForm = ProfilePictureForm()
        notifications = current_user.unreadNotifications()
        return dict(passwordChangeForm=passwordChangeForm,
                    avatarChangeForm=avatarChangeForm,
                    notifications=notifications)
    else:
        login_form = LoginForm()
        return dict(login_form=login_form)

# # Make sure schools is populated
# from nexnest.data import school_gen


# Flask Admin Setup
from flask_admin import Admin

admin = Admin(app, name='Nexnest', template_mode='bootstrap3')

# Flask Admin Model Views
from flask_admin.contrib.sqla import ModelView


class AdminModelView(ModelView):
    def is_accessible(self):
        return True
        # return current_user.isAdmin # TURN ON FOR PRODUCTION

    def inaccessible_callback(self, name, **kwargs):
        # redirect to login page if user doesn't have access
        return redirect(url_for('indexs.index'))


admin.add_view(AdminModelView(User, session))
admin.add_view(AdminModelView(Group, session))
admin.add_view(AdminModelView(Listing, session))
admin.add_view(AdminModelView(Message, session))
admin.add_view(AdminModelView(Landlord, session))
admin.add_view(AdminModelView(School, session))
admin.add_view(AdminModelView(Tour, session))
admin.add_view(AdminModelView(TourMessage, session))
admin.add_view(AdminModelView(GroupMessage, session))
admin.add_view(AdminModelView(DirectMessage, session))
admin.add_view(AdminModelView(GroupListing, session))
admin.add_view(AdminModelView(Notification, session))
