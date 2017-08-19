import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'domislove'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True

    UPLOAD_FOLDER = basedir + '/nexnest/uploads'
    ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif', 'pdf'])
    TRAP_BAD_REQUEST_ERRORS = True

    ADMINS = ['staff@nexnest.com']

    # SERVER_NAME = '127.0.0.1:8000' # BREAKS CSRF TOKENS FOR LOCAL
    SECURITY_PASSWORD_SALT = os.environ.get('SECURITY_PASSWORD_SALT')
    # 'gc7L9UYJKqVyTMoEPbDhzGZhwogXL7Eb2hRuiRPoyhEb7uucgWUzwjWi5cLo86dX'
    GOOGLE_MAPS_KEY = os.environ.get('GOOGLE_MAPS_KEY')
    # 'AIzaSyACeJxqY35gOjqNTIukZb6A6Zh6jvQnY3w'
    BRAINTREE_MERCHANT_ID = os.environ.get('BRAINTREE_MERCHANT_ID') or '95d9g95dztdsgkkh'
    BRAINTREE_PUBLIC_KEY = os.environ.get('BRAINTREE_PUBLIC_KEY') or 'fdtk8w9qbpvqr6kn'
    BRAINTREE_PRIVATE_KEY = os.environ.get('BRAINTREE_PRIVATE_KEY') or 'ec367f7335d5e9c222656212e1ff78f2'

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    @classmethod
    def init_app(cls, app):
        Config.init_app(app)

        # log to syslog
        import logging
        from logging.handlers import SysLogHandler
        syslog_handler = SysLogHandler()
        syslog_handler.setLevel(logging.DEBUG)
        app.logger.addHandler(syslog_handler)
    DEBUG = True
    MAIL_SERVER = 'http://mail.nexnest.com/'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
        'postgres://nexnest_development:domislove@localhost:5432/nexnest_development'


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or \
        'postgres://nexnest_test:domislove@localhost:5432/nexnest_test'


class ProductionConfig(Config):
    @classmethod
    def init_app(cls, app):
        Config.init_app(app)
    # MAIL SERVER CONFIG
    MAIL_SERVER = 'mail.nexnest.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data.sqlite')


class UnixConfig(ProductionConfig):
    @classmethod
    def init_app(cls, app):
        ProductionConfig.init_app(app)

        # log to syslog
        import logging
        from logging.handlers import SysLogHandler
        syslog_handler = SysLogHandler()
        syslog_handler.setLevel(logging.WARNING)
        app.logger.addHandler(syslog_handler)


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig,
    'unix': UnixConfig
}
