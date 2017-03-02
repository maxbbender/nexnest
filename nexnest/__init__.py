# Nexnest Application Startpoint

# OS Functions
from os import environ
from os.path import join
from os.path import dirname

from dotenv import load_dotenv

# Flask
from flask import Flask

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

superENV = environ.get('NEXNEST_SUPER_%s_SETTINGS' % env.upper())

if superENV is not None:
    app.config.from_envvar('NEXNEST_SUPER_%s_SETTINGS' % env.upper())
else:
    app.config.from_envvar('NEXNEST_%s_SETTINGS' % env.upper())

app.secret_key = 'domislove'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# app.config['SERVER_NAME'] = '127.0.0.1:8000' # Breaks CSRF TOKENS
