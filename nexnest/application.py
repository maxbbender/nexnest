# Nexnest Application Startpoint

# OS Functions
from os import environ
from os.path import join
from os.path import dirname

from dotenv import load_dotenv

# Flask
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
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

# App setup
app = Flask(__name__)
app.config.from_envvar('NEXNEST_%s_SETTINGS' % env.upper())
app.secret_key = 'domislove'


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

from nexnest.models.user import User
from nexnest.models.school import School
from nexnest.models.listing import Listing
from nexnest.models.group import Group
from nexnest.models.group_listing import GroupListing
from nexnest.models.message import Message
from nexnest.models.group_message import GroupMessage


@login_manager.user_loader
def load_user(user_id):
    return session.query(User).filter_by(id=user_id).first()

# Blueprints
from nexnest.blueprints.index import indexs
from nexnest.blueprints.listing import listings
from nexnest.blueprints.user import users
from nexnest.blueprints.group import groups

app.register_blueprint(indexs)
app.register_blueprint(listings)
app.register_blueprint(users)
app.register_blueprint(groups)

from nexnest.forms.loginForm import LoginForm


@app.context_processor
def insert_login_form():
    login_form = LoginForm()
    return dict(login_form=login_form)

# # Make sure schools is populated
# from nexnest.data import school_gen
