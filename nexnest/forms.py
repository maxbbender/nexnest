from urllib.parse import urlparse, urljoin

from flask import request, url_for, redirect
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired

from wtforms.fields import StringField, PasswordField, SubmitField, BooleanField, IntegerField, TextAreaField, SelectField, DateField, HiddenField

from wtforms.validators import InputRequired, Length, Email, EqualTo, Optional, URL

from nexnest.static.dataSets import *


def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and \
        ref_url.netloc == test_url.netloc


def get_redirect_target():
    for target in request.args.get('next'), request.referrer:
        if not target:
            continue
        if is_safe_url(target):
            return target


class RedirectForm(FlaskForm):
    next = HiddenField()

    def __init__(self, *args, **kwargs):
        FlaskForm.__init__(self, *args, **kwargs)
        if not self.next.data:
            self.next.data = get_redirect_target() or ''

    def redirect(self, endpoint='/', **values):
        if is_safe_url(self.next.data):
            return redirect(self.next.data)
        target = get_redirect_target()
        return redirect(target or url_for(endpoint, **values))


class TourMessageForm(RedirectForm):
    tour_id = HiddenField('Tour ID',
                          [InputRequired("Group ID Field Required")])
    content = TextAreaField('Message',
                            [InputRequired("You must put in a message")])


class TourForm(RedirectForm):
    group_tour_id = HiddenField('group_id', [InputRequired()])
    listing_id = HiddenField('listing_id', [InputRequired()])
    description = TextAreaField('Include a brief message to acompany your tour request',
                                [Length(min=1, max=1500), InputRequired()])
    requestedDateTime = HiddenField('Date and time you would like to tour the house', validators=[InputRequired()])


class TourDateChangeForm(RedirectForm):
    input_id = HiddenField('group_id', [InputRequired()])
    requestedDateTime = HiddenField(
        'Date and time you would like to tour the house')


class SuggestListingForm(RedirectForm):
    group_id = HiddenField('group_id', [InputRequired()])
    listing_id = HiddenField('listing_id', [InputRequired()])


class RegistrationForm(RedirectForm):
    email = StringField('Email',
                        [InputRequired("You must enter an email address"),
                         Email("Email must be valid format")])
    password = PasswordField('Password',
                             [InputRequired(),
                              EqualTo('confirm',
                                      message="Passwords must match")])
    confirm = PasswordField('Confirm Password', [InputRequired()])

    fname = StringField('First Name', [InputRequired()])
    lname = StringField('Last Name', [InputRequired()])
    school = SelectField('School', [Optional()], choices=schools)
    landlord = HiddenField('Landlord')
    submit = SubmitField('Register')


class LandlordMoreInfoForm(RedirectForm):
    date_of_birth = DateField('Date of Birth', [InputRequired()])
    date_of_birth = HiddenField('Date of Birth', [InputRequired()])
    street = StringField('Street Address', [
                         Length(min=2, max=50), InputRequired()])
    city = StringField('City', [Length(min=2, max=50), InputRequired()])
    state = SelectField('State', choices=statesLong)
    zip_code = StringField('Zipcode', [Length(min=5, max=5), InputRequired()])
    user_id = HiddenField('user')
    availabilities = HiddenField('availabilities', validators=[Optional()])
    check_pay = BooleanField('Do you accept rent payments via checks?')
    online_pay = BooleanField('Do you accept rent payments through NexNest?')


class ProfilePictureForm(RedirectForm):
    profilePicture = FileField('Profile Picture', validators=[FileRequired()])


class LoginForm(RedirectForm):
    email = StringField('Email Address', [Length(min=6, max=35)])
    password = PasswordField('Password', [InputRequired()])
    nextURL = HiddenField('Next', [Optional()])


class ListingForm(RedirectForm):
    street = StringField('Street Address', [
                         Length(min=2, max=50), InputRequired()])
    apartment_number = IntegerField('Apartment Number', [Optional()])
    city = StringField('City', [Length(min=2, max=50), InputRequired()])
    state = SelectField('State', choices=statesLong)
    zip_code = StringField('Zipcode', [Length(min=5, max=5), InputRequired()])
    start_date = StringField(
        'Start Date', [Length(min=5, max=15), InputRequired()])
    end_date = StringField(
        'End Date', [Length(min=5, max=15), InputRequired()])
    time_period = SelectField('Length of Lease', choices=valid_time_periods)
    time_period_date_range = HiddenField('Lease Time Frame', [InputRequired()])
    num_bedrooms = IntegerField('Number of Bedrooms', [InputRequired()])
    num_full_baths = IntegerField(
        'Number of Full Bathrooms', [InputRequired()])
    num_half_baths = IntegerField(
        'Number of Half Bathrooms', [Optional()])
    price = IntegerField('Price per Bedroom per Semester', [InputRequired()])
    square_footage = IntegerField('Square Footage of House', [Optional()])
    parking = SelectField('What Parking is Available',
                          choices=valid_parking_types)
    cats = BooleanField('Are Cats Allowed?')
    dogs = BooleanField('Are Dogs Allowed?')
    other_pets = TextAreaField('Are Other Pets Allowed?', [
        Length(min=0, max=160)])
    washer = BooleanField('Is there a Washing Machine?')
    dryer = BooleanField('Is there a Dryer?')
    dishwasher = BooleanField('Is there a Dishwasher?')
    air_conditioning = BooleanField('Is there Air Conditioning?')
    handicap = BooleanField('Is the property handicap accessible?')
    furnished = BooleanField('Is the property furnished?')
    emergency_maintenance = BooleanField(
        'Do you provide emergency maintenance?')
    snow_plowing = BooleanField('Do you provide snow removal?')
    garbage_service = BooleanField('Is garbage service included?')
    security_service = BooleanField('Is there a security service provided?')
    description = TextAreaField('Please provide a detailed description of the property', [
                                Length(min=0, max=1500), Optional()])
    property_type = SelectField('Property Type', choices=propertyTypes)
    rent_due = SelectField('How often is rent due?', choices=rentDue)
    first_semester_rent_due_date = DateField(
        'What date is rent due for the first semester?', [Optional()])
    second_semester_rent_due_date = DateField(
        'What date is rent due for the second semester?', [Optional()])
    monthly_rent_due_date = DateField(
        'What day of month is rent due?', [Optional()])
    electricity = BooleanField('Electricity')
    internet = BooleanField('Internet')
    water = BooleanField('Water')
    heat_gas = BooleanField('Heat/Gas')
    cable = BooleanField('Cable')
    washer_free = BooleanField('Is the Washer Free?')
    floor_plan = FileField('Floor Plan')
    youtube_url = StringField('Listing Video', [Optional(), URL()])
    colleges = HiddenField('Colleges', [InputRequired()])
    pictures = FileField('Pictures for Listing')
    bannerPicture = FileField('Pictures for Listing')


class PhotoForm(RedirectForm):
    pictures = FileField('Pictures for Listing')
    bannerPicture = FileField('Pictures for Listing')
    nextAction = HiddenField('Next')


class CreateGroupForm(RedirectForm):
    name = StringField('Group Name:', [Length(min=2, max=50), InputRequired()])
    time_frame = SelectField(
        'When are you looking to rent?', choices=valid_time_frames)
    #start_date = DateField('Start Date', format='%Y-%m-%d')
    #end_date = DateField('End Date', format='%Y-%m-%d')


class GroupMessageForm(RedirectForm):
    group_id = HiddenField(
        'groupID', [InputRequired("Group ID Field Required")])
    content = TextAreaField(
        'Message', [InputRequired("You must put in a message")])


class DirectMessageForm(RedirectForm):
    target_user_id = HiddenField('Target User', [InputRequired()])
    content = TextAreaField('Message', [InputRequired("Message is required")])


class EditAccountForm(RedirectForm):
    fname = StringField(
        'First Name', [InputRequired()])
    lname = StringField(
        'Last Name', [InputRequired()])
    school = SelectField('School', [Optional()], choices=schools)
    email = StringField('Email',
                        [InputRequired("You must enter an email address"),
                         Email("Email must be valid format")])


class LandlordEditAccountForm(EditAccountForm):
    online_pay = BooleanField('Accept Online Payments')
    check_pay = BooleanField('Accept Check Payments')
    street = StringField('Street Address')
    city = StringField('City')
    state = SelectField('State', choices=statesLong)
    zip_code = StringField('Zip Code')
    date_of_birth = HiddenField('Date of Birth', [InputRequired()])
    phone = StringField('Phone Number')


class InviteGroupForm(RedirectForm):
    group_id = HiddenField('group_id', [InputRequired()])
    user_id = HiddenField('user_id', [InputRequired()])


class PasswordChangeForm(RedirectForm):
    oldPassword = PasswordField('Old Password', [InputRequired()])

    newPassword = PasswordField('New Password',
                                [InputRequired(),
                                 EqualTo('newPasswordConfirm',
                                         message="Passwords must match")])
    newPasswordConfirm = PasswordField('Confirm New Password', [InputRequired()])


class GroupListingForm(RedirectForm):
    groupID = HiddenField('groupID', [InputRequired()])
    listingID = HiddenField('listingID', [InputRequired()])
    reqDescription = TextAreaField(
        'Aything you would like to say to the landlord to go along with your request', [InputRequired()])


class GroupListingMessageForm(RedirectForm):
    groupListingID = HiddenField('groupID', [InputRequired()])
    content = TextAreaField('Message',
                            [InputRequired("You must put in a message")])


class HouseMessageForm(RedirectForm):
    houseID = HiddenField('groupID', [InputRequired()])
    content = TextAreaField('Message',
                            [InputRequired("You must put in a message")])


class MaintenanceRequestForm(RedirectForm):
    requestType = SelectField('Request Type', choices=maintenanceRequestTypes)
    details = TextAreaField('Details', [InputRequired()])
    houseID = HiddenField('houseID', [InputRequired()])


class MaintenanceRequestMessageForm(RedirectForm):
    maintenanceID = HiddenField('maintenanceID',
                                validators=[InputRequired()])

    content = TextAreaField('Message',
                            validators=[InputRequired("You must put in a message")])


class LeaseUploadForm(RedirectForm):
    lease = FileField('Lease')

    groupListingID = HiddenField('groupListingID',
                                 validators=[InputRequired()])


class PreCheckoutForm(RedirectForm):
    json = HiddenField('Lease')
    # couponCode = StringField('Coupon Code', validators=[Optional()])


class EmailPreferencesForm(RedirectForm):
    direct_message_email = BooleanField('direct_message')
    tour_message_email = BooleanField('tour_message')
    group_message_email = BooleanField('group_message_email')
    house_message_email = BooleanField('house_message')
    maintenance_message_email = BooleanField('maintenance_message')
    tour_time_email = BooleanField('tour_time_email')
    tour_confirmed_email = BooleanField('tour_confirmed')
    tour_denied_email = BooleanField('tour_denied')
    tour_create_email = BooleanField('tour_create')
    maintenance_email = BooleanField('maintenance')
    maintenance_inProgress_email = BooleanField('maintenance_inProgress')
    maintenance_completed_email = BooleanField('maintenance_completed')
    rent_due_email = BooleanField('rent_due')
    rent_paid_email = BooleanField('rent_paid')
    group_user_email = BooleanField('group_user')
    group_listing_email = BooleanField('group_listing')
    house_email = BooleanField('house')
    group_listing_accept_email = BooleanField('group_listing_accept')
    group_listing_deny_email = BooleanField('group_listing_deny')
    direct_message_notification = BooleanField('direct_message')
    tour_message_notification = BooleanField('tour_message')
    group_message_notification = BooleanField('group_message_email')
    house_message_notification = BooleanField('house_message')
    maintenance_message_notification = BooleanField('maintenance_message')
    tour_time_notification = BooleanField('tour_time_email')
    tour_confirmed_notification = BooleanField('tour_confirmed')
    tour_denied_notification = BooleanField('tour_denied')
    tour_create_notification = BooleanField('tour_create')
    maintenance_notification = BooleanField('maintenance')
    maintenance_inProgress_notification = BooleanField('maintenance_inProgress')
    maintenance_completed_notification = BooleanField('maintenance_completed')
    rent_due_notification = BooleanField('rent_due')
    rent_paid_notification = BooleanField('rent_paid')
    group_user_notification = BooleanField('group_user')
    group_listing_notification = BooleanField('group_listing')
    house_notification = BooleanField('house')
    group_listing_accept_notification = BooleanField('group_listing_accept')
    group_listing_deny_notification = BooleanField('group_listing_deny')


class ReportForm(RedirectForm):
    title = StringField('Subject of Report', validators=[Optional()])
    content = TextAreaField('Describe what went wrong or the feedback you have!', validators=[InputRequired()])
    sourceURL = StringField('The URL of where you had your issue if any', validators=[Optional()])


class PlatformReportForm(ReportForm):
    pass


class ListingReportForm(ReportForm):
    listing_id = HiddenField('listingID', validators=[InputRequired()])


class LandlordReportForm(ReportForm):
    landlord_id = HiddenField('landlordID', validators=[InputRequired()])


class GroupReportForm(ReportForm):
    group_id = HiddenField('groupID', validators=[InputRequired()])


class LandlordPaymentAccountForm(RedirectForm):
    legalBusinessName = StringField('Legal Business Name', validators=[Optional()])
    taxID = StringField('Tax ID', [Optional()])
    accountNumber = StringField('Recieving Account Number')
    routingNumber = StringField('Routing Number')


class CreateCouponForm(RedirectForm):
    couponKey = StringField('Coupon Key', validators=[InputRequired()])
    unlimited = BooleanField('Unlimited', validators=[Optional()])
    uses = IntegerField('Number of Uses', validators=[Optional()])
    percentageOff = IntegerField('Percentage Off (15 would be 15% off)')


class ContactForm(RedirectForm):
    name = StringField('Full Name')
    phone = StringField('Phone Number', validators=[Optional()])
    message = TextAreaField('Message')
