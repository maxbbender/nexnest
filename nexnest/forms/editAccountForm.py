from flask_wtf import FlaskForm
from wtforms.fields import StringField, PasswordField, TextAreaField
from wtforms.validators import InputRequired, Email, EqualTo, Length


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
