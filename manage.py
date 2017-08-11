from flask_script import Manager, Shell
from flask_migrate import MigrateCommand


from nexnest import app

from nexnest.application import db

manager = Manager(app)


def _make_context():
    return dict(app=app, db=db)


manager.add_command('shell', Shell(make_context=_make_context))
manager.add_command('db', MigrateCommand)


if __name__ == "__main__":
    manager.run()
