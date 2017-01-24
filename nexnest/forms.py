from flask_wtf import FlaskForm
from wtforms.fields import StringField, PasswordField, SubmitField, BooleanField, IntegerField, TextAreaField, SelectField, DateField, HiddenField

from flask_wtf.file import FileField, FileRequired

from wtforms.validators import InputRequired, Length, Email, EqualTo

from nexnest.static.dataSets import valid_time_periods, valid_parking_types, valid_unit_types, states


class TourMessageForm(FlaskForm):
    tour_id = HiddenField('Tour ID',
                          [InputRequired("Group ID Field Required")])
    content = TextAreaField('Message',
                            [InputRequired("You must put in a message")])


class TourForm(FlaskForm):
    group_id = HiddenField('group_id', [InputRequired()])
    listing_id = HiddenField('listing_id', [InputRequired()])
    description = TextAreaField('Message to Landlord', [Length(min=1, max=1500), InputRequired()])
    requestedDateTime = HiddenField('Date and time you would like to tour the house')


class TourDateChangeForm(FlaskForm):
    input_id = HiddenField('group_id', [InputRequired()])
    requestedDateTime = HiddenField('Date and time you would like to tour the house')


class SuggestListingForm(FlaskForm):
    group_id = HiddenField('group_id', [InputRequired()])
    listing_id = HiddenField('listing_id', [InputRequired()])


class RegistrationForm(FlaskForm):
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


class ProfilePictureForm(FlaskForm):
    profilePicture = FileField('Profile Picture', validators=[FileRequired()])


class LoginForm(FlaskForm):
    email = StringField('Email Address', [Length(min=6, max=35)])
    password = PasswordField('Password', [InputRequired()])


class ListingForm(FlaskForm):
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


class CreateGroupForm(FlaskForm):
    name = StringField('Group Name:', [Length(min=2, max=50), InputRequired()])
    # time_frame = SelectField(
    #     'When are you looking for a house?', choices=valid_time_frames)
    start_date = DateField('Start Date', format='%Y-%m-%d')
    end_date = DateField('End Date', format='%Y-%m-%d')


class GroupMessageForm(FlaskForm):
    group_id = HiddenField(
        'groupID', [InputRequired("Group ID Field Required")])
    content = TextAreaField(
        'Message', [InputRequired("You must put in a message")])


class DirectMessageForm(FlaskForm):
    target_user_id = HiddenField('Target User', [InputRequired()])
    content = TextAreaField('Message', [InputRequired("Message is required")])


class EditAccountForm(FlaskForm):
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


class InviteGroupForm(FlaskForm):
    group_id = HiddenField('group_id', [InputRequired()])
    user_id = HiddenField('user_id', [InputRequired()])
