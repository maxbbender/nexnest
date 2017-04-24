# Nexnest Application Startpoint

# OS Functions
from os import environ
from os.path import join, dirname

from dotenv import load_dotenv

# Flask
from flask import Flask
from flask_mail import Mail, email_dispatched

import logging
import sys

# DotEnv Setup
load_dotenv(join(dirname(__file__), '..', '.env'))

# Environment choice
env = environ.get('NEXNEST_ENV')

if env is None:
    env = 'development'

# App setup
app = Flask(__name__, static_folder="static")
app.config.from_object('nexnest.config')

superENV = environ.get('NEXNEST_SUPER_%s_SETTINGS' % env.upper())

if superENV is not None:
    app.config.from_envvar('NEXNEST_SUPER_%s_SETTINGS' % env.upper())
else:
    app.config.from_envvar('NEXNEST_%s_SETTINGS' % env.upper())


# - LOGGER -
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

ch = logging.StreamHandler(sys.stdout)
ch.setLevel(logging.DEBUG)

# create formatter and add it to the handlers
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

ch.setFormatter(formatter)

# add the handlers to the logger
logger.addHandler(ch)

mail = Mail(app)


def logEmailDispatch(message, app):
    logger.debug('Email Sent! Subject %s' % message.subject)


email_dispatched.connect(logEmailDispatch)
