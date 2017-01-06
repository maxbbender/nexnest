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

# Flask Security
from flask.ext.security import Security, SQLAlchemyUserDatastore, AnonymousUser

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

# Blueprints
from nexnest.blueprints.index import indexs
from nexnest.blueprints.registerTenant import registerTenants
from nexnest.blueprints.registerLandlord import registerLandlords

app.register_blueprint(indexs)
app.register_blueprint(registerTenants)
app.register_blueprint(registerLandlords)

# DB setup
engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
session = scoped_session(sessionmaker(bind=engine))
db = SQLAlchemy(app)

# CSRF setup
csrf = CSRFProtect(app)

# Login Manager
# login_manager = LoginManager()
# login_manager.init_app(app)
# login_manager.login_view = '/login'
# login_manager.anonymous_user = AnonymousUser

# Flask Secuirty Setup
from nexnest.models.role import Role
from nexnest.models.user import User
from nexnest.models.user_role import UserRole

user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)
