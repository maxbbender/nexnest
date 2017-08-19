import os

from flask_script import Manager, Shell
from flask_migrate import MigrateCommand

from nexnest import createApp, db


app = createApp(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager(app)


def _make_context():
    from nexnest.models.user import User
    from nexnest.models.availability import Availability
    from nexnest.models.coupon import Coupon
    return dict(app=app, db=db,
                User=User,
                Availability=Availability,
                Coupon=Coupon,
                )


manager.add_command('shell', Shell(make_context=_make_context))
manager.add_command('db', MigrateCommand)


if __name__ == "__main__":
    manager.run()
