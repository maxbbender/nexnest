from os.path import dirname

UPLOAD_FOLDER = dirname(__file__) + '/uploads'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif', 'pdf'])
TRAP_BAD_REQUEST_ERRORS = True

# MAIL SERVER CONFIG
MAIL_SERVER = 'mail.nexnest.com'
MAIL_PORT = 587
MAIL_USE_TLS = True
MAIL_USE_SSL = False
MAIL_USERNAME = 'no_reply@nexnest.com'
MAIL_PASSWORD = 'W3HgnVDXEo'

ADMINS = ['staff@nexnest.com']

TESTING = True
DEBUG = True

SECRET_KEY = '8whZEVOID8G3UzmYDxQn'
# SERVER_NAME = '127.0.0.1:8000' # BREAKS CSRF TOKENS FOR LOCAL
