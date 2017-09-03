import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True

    UPLOAD_FOLDER = basedir + '/nexnest/uploads'
    ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif', 'pdf'])
    TRAP_BAD_REQUEST_ERRORS = True

    ADMINS = ['max@nexnest.com']

    # SERVER_NAME = '127.0.0.1:8000' # BREAKS CSRF TOKENS FOR LOCAL
    SECURITY_PASSWORD_SALT = os.environ.get('SECURITY_PASSWORD_SALT')
    # 'gc7L9UYJKqVyTMoEPbDhzGZhwogXL7Eb2hRuiRPoyhEb7uucgWUzwjWi5cLo86dX'
    GOOGLE_MAPS_KEY = os.environ.get('GOOGLE_MAPS_KEY')
    GOOGLE_CAPTCHA_SECRET = os.environ.get('GOOGLE_CAPTCHA_SECRET')
    FLASK_CONFIG = os.environ.get('FLASK_CONFIG')
    BRAINTREE_MERCHANT_ID = os.environ.get('BRAINTREE_MERCHANT_ID')
    BRAINTREE_PUBLIC_KEY = os.environ.get('BRAINTREE_PUBLIC_KEY')
    BRAINTREE_PRIVATE_KEY = os.environ.get('BRAINTREE_PRIVATE_KEY')
    BRAINTREE_ENV = os.environ.get('BRAINTREE_ENV') or 'sandbox'
    SLACK_LOG_URL = os.environ.get('SLACK_LOG_URL') or 'https://hooks.slack.com/services/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'
    SLACK_WARNING_URL = os.environ.get('SLACK_WARNING_URL')
    SLACK_ERROR_URL = os.environ.get('SLACK_ERROR_URL')

    @staticmethod
    def init_app(app):
        app.logger.handlers = []
        # log to syslog
        import logging
        import sys
        ch = logging.StreamHandler(sys.stdout)
        ch.setLevel(logging.DEBUG)
        formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        ch.setFormatter(formatter)
        app.logger.addHandler(ch)
        pass


class DevelopmentConfig(Config):
    @classmethod
    def init_app(cls, app):
        Config.init_app(app)
        import logging
        from slack_log_handler import SlackLogHandler
        slackHandler = SlackLogHandler(Config.SLACK_LOG_URL)
        slackHandler.setLevel(logging.WARNING)
        app.logger.addHandler(slackHandler)
    DEBUG = True
    MAIL_SERVER = 'mail.nexnest.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False
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

        app.logger.handlers = []

        import logging
        from logging.handlers import RotatingFileHandler
        from slack_log_handler import SlackLogHandler

        # Slack Warning
        slackWarningHandler = SlackLogHandler(Config.SLACK_WARNING_URL) or Config.SLACK_LOG_URL
        slackWarningHandler.setLevel(logging.WARNING)
        app.logger.addHandler(slackWarningHandler)

        # Slack Error
        slackErrHandler = SlackLogHandler(Config.SLACK_ERROR_URL) or Config.SLACK_LOG_URL
        slackErrHandler.setLevel(logging.ERROR)
        app.logger.addHandler(slackErrHandler)

        # Debug Handler
        debugHandler = RotatingFileHandler('/var/log/nexnest/debug.log', maxBytes=10000, backupCount=5)
        debugHandler.setLevel(logging.DEBUG)
        app.logger.addHandler(debugHandler)

        # Info Handler
        infoHandler = RotatingFileHandler('/var/log/nexnest/info.log', maxBytes=10000, backupCount=5)
        infoHandler.setLevel(logging.INFO)
        app.logger.addHandler(infoHandler)

    # MAIL SERVER CONFIG
    MAIL_SERVER = 'mail.nexnest.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    DEBUG = False
    TESTING = False


class UnixConfig(ProductionConfig):
    @classmethod
    def init_app(cls, app):
        ProductionConfig.init_app(app)

        # log to syslog
        import logging
        from logging.handlers import SysLogHandler
        syslog_handler = SysLogHandler(address='/var/log/nexnest.log')
        syslog_handler.setLevel(logging.WARNING)
        app.logger.addHandler(syslog_handler)



class MacConfig(DevelopmentConfig):
    @classmethod
    def init_app(cls,app):
        # app.logger.handlers = []
        # import logging
        # from logging.handlers import SysLogHandler
        # syslog_handler = SysLogHandler(address='/var/log/nexnest.log')
        # syslog_handler.setLevel(logging.WARNING)
        # app.logger.addHandler(syslog_handler)
        pass




config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig,
    'unix': UnixConfig,
    'mac': MacConfig
}
