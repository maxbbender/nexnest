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

# Blueprints
from nexnest.blueprints.index import indexs
from nexnest.blueprints.registerTenant import registerTenants
from nexnest.blueprints.registerLandlord import registerLandlords
from nexnest.blueprints.users import users

app.register_blueprint(indexs)
app.register_blueprint(registerTenants)
app.register_blueprint(registerLandlords)
app.register_blueprint(users)

from nexnest.forms.loginForm import LoginForm


@app.context_processor
def insert_login_form():
    login_form = LoginForm()
    return dict(login_form=login_form)
