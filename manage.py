import os

from flask_script import Manager, Shell
from flask_migrate import MigrateCommand

from nexnest import createApp

from nexnest.application import db
from nexnest.models import *

app = createApp(os.getenv('FLASK_CONFIG' or 'default'))
manager = Manager(app)


def _make_context():
    return dict(app=app, db=db,
                User=user.User,
                Availability=availability.Availability,
                Coupon=coupon.Coupon,
                )


manager.add_command('shell', Shell(make_context=_make_context))
manager.add_command('db', MigrateCommand)


if __name__ == "__main__":
    manager.run()
