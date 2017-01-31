from flask import request, url_for, redirect
from flask_wtf import FlaskForm
from wtforms.fields import StringField, PasswordField, SubmitField, BooleanField, IntegerField, TextAreaField, SelectField, DateField, HiddenField

from flask_wtf.file import FileField, FileRequired

from wtforms.validators import InputRequired, Length, Email, EqualTo

from nexnest.static.dataSets import valid_time_periods, valid_parking_types, valid_unit_types, states

from urllib.parse import urlparse, urljoin


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

    def redirect(self, endpoint='index', **values):
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
    description = TextAreaField('Message to Landlord', [Length(min=1, max=1500), InputRequired()])
    requestedDateTime = HiddenField('Date and time you would like to tour the house')


class TourDateChangeForm(RedirectForm):
    input_id = HiddenField('group_id', [InputRequired()])
    requestedDateTime = HiddenField('Date and time you would like to tour the house')


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
    school = StringField('School', [InputRequired()])
    submit = SubmitField('Register')


class ProfilePictureForm(RedirectForm):
    profilePicture = FileField('Profile Picture', validators=[FileRequired()])


class LoginForm(RedirectForm):
    email = StringField('Email Address', [Length(min=6, max=35)])
    password = PasswordField('Password', [InputRequired()])


class ListingForm(RedirectForm):
    street = StringField('Street Address', [Length(min=2, max=50), InputRequired()])
    apartment_number = IntegerField('Apartment Number', [InputRequired()])
    city = StringField('City', [Length(min=2, max=50), InputRequired()])
    state = SelectField('State', choices=states)
    zip_code = StringField('Zipcode', [Length(min=5, max=5), InputRequired()])
    start_date = StringField('Start Date', [Length(min=5, max=15), InputRequired()])
    end_date = StringField('End Date', [Length(min=5, max=15), InputRequired()])
    time_period = SelectField('Length of Lease', choices=valid_time_periods)
    unit_type = SelectField('Unit Type', choices=valid_unit_types)
    num_bedrooms = IntegerField('Number of Bedrooms', [InputRequired()])
    num_full_baths = IntegerField('Number of Full Bathrooms', [InputRequired()])
    num_half_baths = IntegerField('Number of Half Bathrooms', [InputRequired()])
    price = IntegerField('Price per Bedroom per Semester', [InputRequired()])
    square_footage = IntegerField('Square Footage of House', [InputRequired()])
    parking = SelectField('What Parking is Available', choices=valid_parking_types)
    cats = BooleanField('Are Cats Allowed?')
    dogs = BooleanField('Are Dogs Allowed?')
    other_pets = BooleanField('Are Other Pets Allowed?')
    washer = BooleanField('Is there a Washing Machine?')
    dryer = BooleanField('Is there a Dryer?')
    dishwasher = BooleanField('Is there a Dishwasher?')
    air_conditioning = BooleanField('Is there Air Conditioning?')
    handicap = BooleanField('Is the property handicap accessible?')
    furnished = BooleanField('Is the property furnished?')
    utilities_included = BooleanField('Are utilities included in the price?')
    emergency_maintenance = BooleanField('Do you provide emergency maintenance?')
    snow_plowing = BooleanField('Do you provide snow removal?')
    garbage_service = BooleanField('Is garbage service included?')
    security_service = BooleanField('Is there a security service provided?')
    description = TextAreaField('Please provide a detailed description of the property', [Length(min=1, max=1500), InputRequired()])


class CreateGroupForm(RedirectForm):
    name = StringField('Group Name:', [Length(min=2, max=50), InputRequired()])
    # time_frame = SelectField(
    #     'When are you looking for a house?', choices=valid_time_frames)
    start_date = DateField('Start Date', format='%Y-%m-%d')
    end_date = DateField('End Date', format='%Y-%m-%d')


class GroupMessageForm(RedirectForm):
    group_id = HiddenField(
        'groupID', [InputRequired("Group ID Field Required")])
    content = TextAreaField(
        'Message', [InputRequired("You must put in a message")])


class DirectMessageForm(RedirectForm):
    target_user_id = HiddenField('Target User', [InputRequired()])
    content = TextAreaField('Message', [InputRequired("Message is required")])


class EditAccountForm(RedirectForm):
    fname = StringField('First Name', [InputRequired()])
    lname = StringField('Last Name', [InputRequired()])
    school = StringField('School Attending')
    dob = StringField('Date of Birth')
    bio = TextAreaField('If you wish provide a short personal bio')
    phone = StringField('Phone Number', [Length(min=10, max=10)])
    website = StringField('Your personal website url')
    email = StringField('Email',
                        [InputRequired("You must enter an email address"),
                         Email("Email must be valid format")])


class InviteGroupForm(RedirectForm):
    group_id = HiddenField('group_id', [InputRequired()])
    user_id = HiddenField('user_id', [InputRequired()])


class PasswordChangeForm(RedirectForm):
    oldPassword = PasswordField('Old Password', [InputRequired()])

    newPassword = PasswordField('Password',
                                [InputRequired(),
                                 EqualTo('newPasswordConfirm',
                                         message="Passwords must match")])
    newPasswordConfirm = PasswordField('Confirm Password', [InputRequired()])


class GroupListingForm(RedirectForm):
    groupID = HiddenField('groupID', [InputRequired()])
    listingID = HiddenField('listingID', [InputRequired()])
    reqDescription = TextAreaField('Aything you would like to say to the landlord to go along with your request', [InputRequired()])


class GroupListingMessageForm(RedirectForm):
    groupListingID = HiddenField('groupID', [InputRequired()])
    content = TextAreaField('Message',
                            [InputRequired("You must put in a message")])
