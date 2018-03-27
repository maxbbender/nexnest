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
    from nexnest.models.house import House
    from nexnest.models.group import Group
    from nexnest.models.listing import Listing
    from nexnest.models.listing_school import ListingSchool
    return dict(app=app, db=db,
                User=User,
                Availability=Availability,
                Coupon=Coupon,
                House=House,
                Group=Group,
                Listing=Listing,
                ListingSchool=ListingSchool
                )


manager.add_command('shell', Shell(make_context=_make_context))
manager.add_command('db', MigrateCommand)


@manager.command
def dataCreate():
    import nexnest.data_gen.school_gen
    import nexnest.data_gen.dummy_data


@manager.command
def get_all_users():
    from nexnest.models.user import User

    with open('all_users.txt', "w+") as file:
        # Max Bender - maxbbender@gmail.com - Email Confirmed (False)

        for user in User.query.all():
            print_string = '%s %s - %s - Email Confirmed (%r)\r\n' % (user.fname, user.lname, user.email, user.email_confirmed)
            file.truncate()
            file.write(print_string)
            print(print_string)


@manager.command
def get_all_tentant_users():
    from nexnest.models.user import User

    with open('all_tenants.txt', "w+") as file:
        # Max Bender - maxbbender@gmail.com - Email Confirmed (False)

        for user in User.query.all():
            if not user.isLandlord:
                print_string = '%s %s - %s - Email Confirmed (%r)\r\n' % (user.fname, user.lname, user.email, user.email_confirmed)
                file.truncate()
                file.write(print_string)
                print(print_string)


@manager.command
def get_unconfirmed_users():
    from nexnest.models.user import User

    with open('unconfirmed_users.txt', "w+") as file:
        # Max Bender - maxbbender@gmail.com - Email Confirmed (False)

        for user in User.query.filter_by(email_confirmed=False).all():
            response_string = '%s %s - %s - Email Confirmed (%r)\r\n' % (user.fname, user.lname, user.email, user.email_confirmed)
            file.truncate()
            file.write(response_string)
            print(response_string)


@manager.command
def get_landlords():
    from nexnest.models.user import User
    from nexnest.models.landlord import Landlord

    with open('landlords.txt', "w+") as file:
        # Max Bender - maxbbender@gmail.com - Email Confirmed (False)

        for landlord in Landlord.query.all():
            user = landlord.user
            response_string = '%s %s - %s - Email Confirmed (%r) - IsLandlord(%r)\r\n' % (user.fname, user.lname, user.email, user.email_confirmed, user.isLandlord)
            file.truncate()
            file.write(response_string)
            print(response_string)


if __name__ == "__main__":
    manager.run()
