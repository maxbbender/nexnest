# Nexnest Application Startpoint

# OS Functions
from os import environ
from os.path import join
from os.path import dirname

from dotenv import load_dotenv

# Flask
from flask import Flask

import logging
import sys

# DotEnv Setup
load_dotenv(join(dirname(__file__), '..', '.env'))

# Environment choice
env = environ.get('NEXNEST_ENV')

if env is None:
    env = 'development'

# File Uploads
UPLOAD_FOLDER = dirname(__file__) + '/uploads'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif', 'pdf'])

# App setup
app = Flask(__name__, static_folder="static")

superENV = environ.get('NEXNEST_SUPER_%s_SETTINGS' % env.upper())

if superENV is not None:
    app.config.from_envvar('NEXNEST_SUPER_%s_SETTINGS' % env.upper())
else:
    app.config.from_envvar('NEXNEST_%s_SETTINGS' % env.upper())

app.secret_key = 'domislove'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['TRAP_BAD_REQUEST_ERRORS'] = True
# app.config['SERVER_NAME'] = '127.0.0.1:8000' # Breaks CSRF TOKENS

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
# create file handler which logs even debug messages
# fh = logging.FileHandler('spam.log')
# fh.setLevel(logging.DEBUG)
# create console handler with a higher log level
ch = logging.StreamHandler(sys.stdout)
ch.setLevel(logging.DEBUG)
# create formatter and add it to the handlers
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
# fh.setFormatter(formatter)
ch.setFormatter(formatter)
# add the handlers to the logger
# logger.addHandler(fh)
logger.addHandler(ch)
