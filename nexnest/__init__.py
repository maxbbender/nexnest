# Nexnest Application Startpoint

# OS Functions
import os
from os import environ
from os.path import join, dirname, exists

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


# print(join(os.path.dirname(os.path.realpath(__file__)), 'log', 'error.log'))

if not exists(join(os.path.dirname(os.path.realpath(__file__)), 'log', 'error.log')):
    with open(join(os.path.dirname(os.path.realpath(__file__)), 'log', 'error.log'), 'w') as f:
        f.write('')


if not exists(join(os.path.dirname(os.path.realpath(__file__)), 'log', 'debug.log')):
    with open(join(os.path.dirname(os.path.realpath(__file__)), 'log', 'debug.log'), 'w') as f:
        f.write('')


errorHandler = logging.FileHandler(join(os.path.dirname(os.path.realpath(__file__)), 'log', 'error.log'), 'r+')
errorHandler.setLevel(logging.ERROR)

errorHandlerD = logging.FileHandler(join(os.path.dirname(os.path.realpath(__file__)), 'log', 'debug.log'), 'r+')
errorHandlerD.setLevel(logging.DEBUG)

# create formatter and add it to the handlers
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

ch.setFormatter(formatter)
errorHandler.setFormatter(formatter)
errorHandlerD.setFormatter(formatter)

# add the handlers to the logger
logger.addHandler(ch)
logger.addHandler(errorHandler)
logger.addHandler(errorHandlerD)

mail = Mail(app)


def logEmailDispatch(message, app):
    logger.debug('Email Sent! Subject %s | Text %s' % (message.subject, message.html))


email_dispatched.connect(logEmailDispatch)
